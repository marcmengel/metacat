
# need tests for at least:

def test_metacat_help_(env):
    with os.popen("metacat help ", "r") as fin:
        data = fin.read()
        assert(data.find("metacat") > 0 )
        assert(data.find("auth") > 0 )
        assert(data.find("login") > 0 )
        assert(data.find("version") > 0 )

def test_metacat_version_(env):
    with os.popen("metacat version ", "r") as fin:
        data = fin.read()
        assert(data.find("Server version") > 0)
        assert(data.find("Client version") > 0)

def test_metacat_auth_login(env, token):
    with os.popen(f"metacat auth login -m token {os.environ['USER']}", "r") as fin:
        data = fin.read()
        assert(data.find(os.environ['USER']) > 0)
        assert(data.find("User") >= 0)
        assert(data.find("Expires") >= 0)

def test_metacat_auth_whoami(env):
    with os.popen("metacat auth whoami", "r") as fin:
        data = fin.read()
        assert(data.find(os.environ['USER']) > 0)
        assert(data.find("User") >= 0)
        assert(data.find("Expires") >= 0)

# Not bothering with proxy bits...
#def test_metacat_auth_mydn(env):
#    with os.popen("metacat auth mydn", "r") as fin:
#        data = fin.read()
#        # check output


def test_metacat_auth_list(env):
    with os.popen("metacat auth list", "r") as fin:
        data = fin.read()
        assert(data.find('Token Library'), >= 0)
        assert(data.find('{os.environ["USER"]}/.token_library'), >= 0)
        assert(data.find(os.environ["HYPOT_SERVER_URL"]), >= 0)

def test_metacat_auth_export(env):
    with os.popen("metacat auth export {os.environ['HYPOT_SERVER_URL']}", "r") as fin:
        data = fin.read()
        assert(len(data) > 128)

# punting on this for now... 
#def test_metacat_auth_import(env):
#    with os.popen("metacat auth import", "r") as fin:
#        data = fin.read()
        
# jumping some file delcaration tests first, so we then have some files
# to make datasets of(?) 
def test_metacat_file_declare(env):
    with os.popen("metacat file declare", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_declare-many(env):
    with os.popen("metacat file declare-many", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_dataset_create(env):
    with os.popen("metacat dataset create", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_dataset_show(env):
    with os.popen("metacat dataset show", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_dataset_files(env):
    with os.popen("metacat dataset files", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_dataset_list(env):
    with os.popen("metacat dataset list", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_dataset_add-subset(env):
    with os.popen("metacat dataset add-subset", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_dataset_add-files(env):
    with os.popen("metacat dataset add-files", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_dataset_remove-files(env):
    with os.popen("metacat dataset remove-files", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_dataset_update(env):
    with os.popen("metacat dataset update", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_dataset_remove(env):
    with os.popen("metacat dataset remove", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_namespace_create(env):
    with os.popen("metacat namespace create", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_namespace_list(env):
    with os.popen("metacat namespace list", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_namespace_show(env):
    with os.popen("metacat namespace show", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_category_list(env):
    with os.popen("metacat category list", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_category_show(env):
    with os.popen("metacat category show", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_declare(env):
    with os.popen("metacat file declare", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_declare-many(env):
    with os.popen("metacat file declare-many", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_declare-sample(env):
    with os.popen("metacat file declare-sample", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_move(env):
    with os.popen("metacat file move", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_add(env):
    with os.popen("metacat file add", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_datasets(env):
    with os.popen("metacat file datasets", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_update(env):
    with os.popen("metacat file update", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_update-meta(env):
    with os.popen("metacat file update-meta", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_retire(env):
    with os.popen("metacat file retire", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_name(env):
    with os.popen("metacat file name", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_fid(env):
    with os.popen("metacat file fid", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_file_show(env):
    with os.popen("metacat file show", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_query_-q(env):
    with os.popen("metacat query -q", "r") as fin:
        data = fin.read()
        # check output <MQL query file>

def test_metacat_query_"<MQL(env):
    with os.popen("metacat query "<MQL", "r") as fin:
        data = fin.read()
        # check output query>"

def test_metacat_named_query_create(env):
    with os.popen("metacat named_query create", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_named_query_show(env):
    with os.popen("metacat named_query show", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_named_query_list(env):
    with os.popen("metacat named_query list", "r") as fin:
        data = fin.read()
        # check output

def test_metacat_named_query_search(env):
    with os.popen("metacat named_query search", "r") as fin:
        data = fin.read()
        # check output


def test_metacat_validate_[options](env):
    with os.popen("metacat validate [options]", "r") as fin:
        data = fin.read()
        # check output <JSON file with metadata>

