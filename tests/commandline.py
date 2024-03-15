
import os
import time
import pytest
import json

from env import env, token, auth

start_ds = int(time.time())

    
@pytest.fixture
def tst_ds():
    ds = start_ds
    return f"{os.environ['USER']}:tst{ds}"

@pytest.fixture
def tst_file_md_list():
    ds = start_ds
    mdl = []
    for i in range(5):
        fname = f"tst_{ds}_{i}.txt"
        fcont = f"data file {fname}\n"
        with open(fname, "w") as fo:
            fo.write(fcont)
        with os.popen(f"xrdadler32 {fname}", "r") as fi:
            hash_n_name = fi.read()
        fhash, _  = hash_n_name.split(" ")
        mdl.append({ 
           "name": fname,
           "namespace": os.environ["USER"],
           "size": len(fcont),
           "checksums": {"adler32": fhash},
           "metadata": { "f.ds": ds },
        })
    return mdl

# need tests for at least:

def test_metacat_help_(auth):
    with os.popen("metacat help 2>&1 ", "r") as fin:
        data = fin.read()
    print(f"data: '{data}'")
    assert(data.find("metacat") >= 0 )
    assert(data.find("auth") > 0 )
    assert(data.find("login") > 0 )
    assert(data.find("version") > 0 )

def test_metacat_version_(auth):
    with os.popen("metacat version ", "r") as fin:
        data = fin.read()
        assert(data.find("Server version") > 0)
        assert(data.find("Client version") > 0)

# punting on non-token login types for now
#def test_metacat_auth_login_x509(auth, proxy):
#    with os.popen(f"metacat auth login -m x509 {os.environ['USER']}", "r") as fin:
#        data = fin.read()
#        assert(data.find(os.environ['USER']) > 0)
#        assert(data.find("User") >= 0)
#        assert(data.find("Expires") >= 0)
#
#def test_metacat_auth_login_services(auth, passwd):
#    with os.popen(f"metacat auth login -m token {os.environ['USER']}", "r") as fin:
#        data = fin.read()
#        assert(data.find(os.environ['USER']) > 0)
#        assert(data.find("User") >= 0)
#        assert(data.find("Expires") >= 0)

def test_metacat_auth_login_token(auth, token):
    with os.popen(f"metacat auth login -m token {os.environ['USER']}", "r") as fin:
        data = fin.read()
        assert(data.find(os.environ['USER']) > 0)
        assert(data.find("User") >= 0)
        assert(data.find("Expires") >= 0)


def test_metacat_auth_whoami(auth):
    with os.popen("metacat auth whoami", "r") as fin:
        data = fin.read()
        assert(data.find(os.environ['USER']) > 0)
        assert(data.find("User") >= 0)
        assert(data.find("Expires") >= 0)

# Not bothering with proxy bits...
#def test_metacat_auth_mydn(auth):
#    with os.popen("metacat auth mydn", "r") as fin:
#        data = fin.read()
#        # check output


def test_metacat_auth_list(auth):
    with os.popen("metacat auth list", "r") as fin:
        data = fin.read()
        assert(data.find('Token library') >= 0)
        assert(data.find(f'{os.environ["USER"]}/.token_library') >= 0)
        assert(data.find(os.environ["METACAT_SERVER_URL"]) >= 0)

def test_metacat_auth_export(auth):
    with os.popen(f"metacat auth export {os.environ['METACAT_SERVER_URL']}", "r") as fin:
        data = fin.read()
        assert(len(data) > 128)

# punting on this for now... 
#def test_metacat_auth_import(auth):
#    with os.popen("metacat auth import", "r") as fin:
#        data = fin.read()

        
# jumping some file delcaration tests first, so we then have some files
# to make datasets of(?) 
def test_metacat_dataset_create(auth, tst_ds):
    with os.popen(f"metacat dataset create {tst_ds} ", "r") as fin:
        data = fin.read()
    assert(data.find(tst_ds) > 0)
    assert(data.find("ataset") > 0)
    assert(data.find("eated") > 0) # dont fail if they fix spelling of cteated

def test_metacat_file_declare(auth,tst_file_md_list, tst_ds):
    md = tst_file_md_list[0]
    with open("mdf1", "w") as mdf:
        json.dump(md, mdf);
    with os.popen(f"metacat file declare -f mdf1 {tst_ds} ", "r") as fin:
        data = fin.read()
    print(f"got data: '{data}'")
    assert( data.find(os.environ["USER"]) > 0)
    assert( data.find(md["name"]) > 0)

        
def test_metacat_file_declare_many(auth, tst_ds, tst_file_md_list):
    with open("mdf", "w") as mdf:
        json.dump(tst_file_md_list[1:], mdf)
    with os.popen(f"metacat file declare-many mdf {tst_ds}", "r") as fin:
        data = fin.read()
    assert( data.find(os.environ["USER"]) > 0)
    for md in tst_file_md_list[1:]:
        assert( data.find(md["name"]) > 0)


def test_metacat_dataset_show(auth, tst_ds):
    with os.popen(f"metacat dataset show {tst_ds}", "r") as fin:
        data = fin.read()
    ns,dsname = tst_ds.split(":")
    assert( data.find(ns) > 0)
    assert( data.find(dsname) > 0)
    assert( data.find(os.environ["USER"]) > 0)


def test_metacat_dataset_files(auth, tst_ds, tst_file_md_list):
    with os.popen(f"metacat dataset files {tst_ds}", "r") as fin:
        data = fin.read()
    # should list all the files...
    for md in tst_file_md_list:
        assert(data.find( md["name"] ) > 0)


def test_metacat_dataset_list(auth, tst_ds):
    with os.popen(f"metacat dataset list {os.environ['USER']}:*", "r") as fin:
        data = fin.read()
    assert(data.find(tst_ds) >= 0)

#=================  below here is largely unfilled-in ==========================
#  remember to take the x_ off as you fill tghem en

def x_test_metacat_dataset_add_subset(auth):
    with os.popen("metacat dataset add-subset", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_dataset_add_files(auth):
    with os.popen("metacat dataset add-files", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_dataset_remove_files(auth):
    with os.popen("metacat dataset remove-files", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_dataset_update(auth):
    with os.popen("metacat dataset update", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_dataset_remove(auth):
    with os.popen("metacat dataset remove", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_namespace_create(auth):
    with os.popen("metacat namespace create", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_namespace_list(auth):
    with os.popen("metacat namespace list", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_namespace_show(auth):
    with os.popen("metacat namespace show", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_category_list(auth):
    with os.popen("metacat category list", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_category_show(auth):
    with os.popen("metacat category show", "r") as fin:
        data = fin.read()
        # check output


def x_test_metacat_file_declare_sample(auth):
    with os.popen("metacat file declare-sample", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_file_move(auth):
    with os.popen("metacat file move", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_file_add(auth):
    with os.popen("metacat file add", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_file_datasets(auth):
    with os.popen("metacat file datasets", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_file_update(auth):
    with os.popen("metacat file update", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_file_update_meta(auth):
    with os.popen("metacat file update-meta", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_file_retire(auth):
    with os.popen("metacat file retire", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_file_name(auth):
    with os.popen("metacat file name", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_file_fid(auth):
    with os.popen("metacat file fid", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_file_show(auth):
    with os.popen("metacat file show", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_query_q(auth):
    with os.popen("metacat query -q", "r") as fin:
        data = fin.read()
        # check output <MQL query file>

def x_test_metacat_query_mql(auth):
    with os.popen("metacat query", "r") as fin:
        data = fin.read()
        # check output query>"

def x_test_metacat_named_query_create(auth):
    with os.popen("metacat named_query create", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_named_query_show(auth):
    with os.popen("metacat named_query show", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_named_query_list(auth):
    with os.popen("metacat named_query list", "r") as fin:
        data = fin.read()
        # check output

def x_test_metacat_named_query_search(auth):
    with os.popen("metacat named_query search", "r") as fin:
        data = fin.read()
        # check output


def x_test_metacat_validate(auth):
    with os.popen("metacat validate [options]", "r") as fin:
        data = fin.read()
        # check output <JSON file with metadata>

