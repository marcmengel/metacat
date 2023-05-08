# common functionality for Auth, GUI and Data servers

from wsdbtools import ConnectionPool
from metacat.util import to_str, to_bytes
from metacat.auth import BaseDBUser, \
    SignedToken, SignedTokenExpiredError, SignedTokenImmatureError, SignedTokenUnacceptedAlgorithmError, SignedTokenSignatureVerificationError
import psycopg2, json, time, secrets, traceback, hashlib, pprint, os, yaml

class AuthenticationCore(WPApp):

    """Class encapsulating the client authentication funtionality for a group
    """

    def __init__(self, cfg):
        self.Cfg = cfg
        db_config = cfg.get("user_database") or cfg["database"]
        connstr = "host=%(host)s port=%(port)s dbname=%(dbname)s user=%(user)s password=%(password)s" % db_config
        self.UserDB = ConnectionPool(postgres=connstr, max_idle_connections=1, idle_timeout=20)
        self.UserDBSchema = db_config.get("schema")

        self.AuthConfig = cfg.get("authentication")
        self.Group = self.AuthConfig("group", "metacat")          
        self.Realm = self.AuthConfig.get("realm", self.Group) # will be used by the rfc2617 authentication
        self.Issuer = self.AuthConfig.get("issuer")
        self.SciTokenIssuers = self.AuthConfig.get("sci_token_issuers", [])
        secret = self.AuthConfig.get("secret")
        if secret is None:    
            raise ValueError("Authentication secret not found in the configuration")
            self.TokenSecret = secrets.token_bytes(128)     # used to sign tokens
        else:         
            h = hashlib.sha256()
            h.update(to_bytes(secret))      
            self.TokenSecret = h.digest()
            
    def auth_config(self, method):
        # configuration for particular authentication mechanism
        return self.AuthConfig.get(method)
                
    def user_db(self):
        conn = self.UserDB.connect()
        if self.UserDBSchema:
            conn.cursor().execute(f"set search_path to {self.UserDBSchema}")
        return conn
        
    TokenExpiration = 24*3600*7

    def verify_token(self, encoded_token):
        try:    
            token = SignedToken.from_bytes(encoded_token)
            #print("verify_token: token:", token.Payload)
            t = time.time()
            #print("   time:", t, "  t-iat:", t-token["iat"], "  t-nbf:", t-token["nbf"])
            token.verify(self.TokenSecret)
            #print("verify_token: verified. subject:", token.subject)
        except SignedTokenExpiredError:
            return None, "Token expired"           
        except SignedTokenImmatureError:
            return None, "Token immature"           
        except SignedTokenUnacceptedAlgorithmError:
            return None, "Invalid token algorithm"           
        except SignedTokenSignatureVerificationError:
            return None, "Token verification failed"           
        except Exception as e:
            return None, str(e)
        else:
            #print("verify_token: token:", token, "  subject:", token.subject)
            return token, None

    def generate_token(self, user, payload={}, expiration=None):
        if expiration is None:
            expiration = self.TokenExpiration
        token = SignedToken(payload, subject=user, expiration=expiration, issuer=self.Issuer)
        #print("generate_token: payload:", token.Payload)
        return token, token.encode(self.TokenSecret)

    def get_digest_password(self, realm, username):
        db = self.connect()
        u = BaseDBUser.get(db, username)
        if u is None:
            return None
        return u.get_password(self.Realm)

    def _auth_digest(self, request_env, redirect):
        # give them cookie with the signed token
        
        ok, data = digest_server(self.Realm, request_env, self.get_digest_password)   # use the Group as realm, if present
        if ok:
            return "ok", None
        elif data:
            return "continue", (401, "Authorization required", {
                'WWW-Authenticate': data
            })
        else:
            return "reject", "Authentication failed"

    def _auth_ldap(self, request, redirect, username):
        if username:
            password = to_str(request.body.strip())
        else:
            username, password = request.body.split(b":",1)
            username = to_str(username)
            password = to_str(password)
        db = self.user_db()
        u = DBUser.get(db, username)
        config = self.App.auth_config(group, "ldap")
        result, reason, expiration = u.authenticate("ldap", config, password)
        if result:
            return "ok", None
        else:
            return "reject", "Authentication failed"

    def accepted_sci_token_issuer(self, issuer):
        return issuer in self.SciTokenIssuers

    def _auth_token(self, request, redirect, username):
        db = self.user_db()
        u = DBUser.get(db, username)
        if u is None:
            return "reject", "Authentication failed"

        encoded = None
        headers = request.headers
        authorization = headers.get("Authorization")
        if authorization:
            try:
                encoded = authorization.split(None, 1)[-1]      # ignore "type", e.g. bearer
            except:
                pass

        if not encoded:
            encoded = request.cookies.get("auth_token") or request.headers.get("X-Authentication-Token")
        if not encoded:
            return "reject", "Authentication failed. Token not found"

        result, reason, expiration = u.authenticate("scitoken", self.App.sciTokenIssuers(self.Group), encoded)
        if not result:
            result, reason, expiration = u.authenticate("jwttoken", 
                    {
                        "issuer": self.App.token_issuer(self.Group),
                        "secret": self.App.token_secret(self.Group)
                    }, encoded)
        if result:
            return "ok", dict(expiration=expiration)
        else:
            return "reject", "Authentication failed"

    def _auth_x509(self, request, redirect, username):
        #log = open("/tmp/_auth_x509.log", "w")
        #print("request.environ:", file=log)
        #for k, v in sorted(request.environ.items()):
        #    print(f"{k}={v}", file=log)
        if request.environ.get("REQUEST_SCHEME") != "https":
            return "HTTPS scheme required\n", 401
            
        db = self.user_db()
        u = DBUser.get(db, username)
        #print("_auth_x509: u:", username, u, file=log)
        result, reason, expiration = u.authenticate("x509", None, request.environ)
        
        if result:
            return "ok", None
        else:
            return "reject", None
        
    def authenticate(self, request, relpath, redirect=None, method="password", username=None, **args):
        #print("method:", method)
        try:
            if method == "x509":
                status, extra = self._auth_x509(request, redirect, username)
            elif method == "digest":
                status, extra = self._auth_digest(request.environ, redirect)
            elif method == "ldap":
                status, extra = self._auth_ldap(request, redirect, username)
            elif method == "token":
                status, extra = self._auth_token(request, redirect, username)
            else:
                return "Unknown authentication method\n", 400
        except:
            traceback.print_exc()
            raise

        if status == "ok":
            return self.App.response_with_auth_cookie(username, redirect, **(extra or {}))
        elif status == "continue":
            return extra
        else:
            return 401, (extra or "Authentication failed") + "\n"

