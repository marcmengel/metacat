import os
import pytest

production = False


@pytest.fixture
def env():
    if production:
        hostaport = "https://metacat.fnal.gov:8143"
        hostport = "https://metacat.fnal.gov:9443"
    else:
        hostaport = "https://metacat.fnal.gov:8143"
        hostport = "http://fermicloud761.fnal.gov:9094"

    os.environ["METACAT_AUTH_SERVER_URL"] = f"{hostaport}/auth/hypot_dev"
    os.environ["DATA_DISPATCHER_URL"] = f"{hostport}/hypot_dd/data"
    os.environ["METACAT_SERVER_URL"] = f"{hostport}/hypot_meta_dev/app"
    os.environ["DATA_DISPATCHER_AUTH_URL"] = f"{hostaport}/auth/hypot_dev"
    os.environ["BEARER_TOKEN_FILE"] = "/tmp/bt_mc_test%d" % os.getpid()
    print("METACAT_SERVER_URL=", os.environ["METACAT_SERVER_URL"])


@pytest.fixture
def token(env):
    os.system("htgettoken -i hypot -a htvaultprod.fnal.gov ")


@pytest.fixture
def auth(token):
    os.system("metacat auth login -m token $USER")
