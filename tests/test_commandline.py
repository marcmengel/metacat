"""
  This file has a commandline based integration test for the metacat
  client and server.

  This suite needs to be run in-order, later tests depend on earlier ones. 
"""
import os
import time
import pytest
import json
import time

from env import env, token, auth, start_ds, tst_ds, tst_file_md_list


# need tests for at least:


def test_metacat_help_(auth):
    with os.popen("metacat help 2>&1 ", "r") as fin:
        data = fin.read()
    print(f"data: '{data}'")
    assert data.find("metacat") >= 0
    assert data.find("auth") > 0
    assert data.find("login") > 0
    assert data.find("version") > 0


def test_metacat_version_(auth):
    with os.popen("metacat version ", "r") as fin:
        data = fin.read()
        assert data.find("Server version") > 0
        assert data.find("Client version") > 0


# punting on non-token login types for now
# def test_metacat_auth_login_x509(auth, proxy):
#    with os.popen(f"metacat auth login -m x509 {os.environ['USER']}", "r") as fin:
#        data = fin.read()
#        assert(data.find(os.environ['USER']) > 0)
#        assert(data.find("User") >= 0)
#        assert(data.find("Expires") >= 0)
#
# def test_metacat_auth_login_services(auth, passwd):
#    with os.popen(f"metacat auth login -m token {os.environ['USER']}", "r") as fin:
#        data = fin.read()
#        assert(data.find(os.environ['USER']) > 0)
#        assert(data.find("User") >= 0)
#        assert(data.find("Expires") >= 0)


def test_metacat_auth_login_token(auth, token):
    with os.popen(f"metacat auth login -m token {os.environ['USER']}", "r") as fin:
        data = fin.read()
        assert data.find(os.environ["USER"]) > 0
        assert data.find("User") >= 0
        assert data.find("Expires") >= 0


def test_delay():
    time.sleep(20)


def test_metacat_auth_whoami(auth):
    with os.popen("metacat auth whoami", "r") as fin:
        data = fin.read()
        assert data.find(os.environ["USER"]) > 0
        assert data.find("User") >= 0
        assert data.find("Expires") >= 0


# Not bothering with proxy bits...
# def test_metacat_auth_mydn(auth):
#    with os.popen("metacat auth mydn", "r") as fin:
#        data = fin.read()
#        # check output


def test_metacat_auth_list(auth):
    with os.popen("metacat auth list", "r") as fin:
        data = fin.read()
        assert data.find("Token library") >= 0
        assert data.find(f'{os.environ["USER"]}/.token_library') >= 0
        assert data.find(os.environ["METACAT_SERVER_URL"]) >= 0


def test_metacat_auth_export(auth):
    with os.popen(
        f"metacat auth export {os.environ['METACAT_SERVER_URL']}", "r"
    ) as fin:
        data = fin.read()
        assert len(data) > 128


# punting on this for now...
# def test_metacat_auth_import(auth):
#    with os.popen("metacat auth import", "r") as fin:
#        data = fin.read()


# jumping some file delcaration tests first, so we then have some files
# to make datasets of(?)
def test_metacat_dataset_create(auth, tst_ds):
    with os.popen(f"metacat dataset create {tst_ds} ", "r") as fin:
        data = fin.read()
    assert data.find(tst_ds) > 0
    assert data.find("ataset") > 0
    assert data.find("eated") > 0  # dont fail if they fix spelling of cteated


def test_metacat_file_declare(auth, tst_file_md_list, tst_ds):
    md = tst_file_md_list[0]
    with open("mdf1", "w") as mdf:
        json.dump(md, mdf)
    with os.popen(f"metacat file declare -f mdf1 {tst_ds} ", "r") as fin:
        data = fin.read()
    print(f"got data: '{data}'")
    os.unlink("mdf1")
    assert data.find(os.environ["USER"]) > 0
    assert data.find(md["name"]) > 0


def test_metacat_file_declare_many(auth, tst_ds, tst_file_md_list):
    with open("mdf", "w") as mdf:
        json.dump(tst_file_md_list[1:], mdf)
    with os.popen(f"metacat file declare-many mdf {tst_ds}", "r") as fin:
        data = fin.read()
    os.unlink("mdf")
    assert data.find(os.environ["USER"]) > 0
    for md in tst_file_md_list[1:]:
        assert data.find(md["name"]) > 0


def test_metacat_dataset_show(auth, tst_ds):
    with os.popen(f"metacat dataset show {tst_ds}", "r") as fin:
        data = fin.read()
    ns, dsname = tst_ds.split(":")
    assert data.find(ns) > 0
    assert data.find(dsname) > 0
    assert data.find(os.environ["USER"]) > 0


def test_metacat_dataset_files(auth, tst_ds, tst_file_md_list):
    with os.popen(f"metacat dataset files {tst_ds}", "r") as fin:
        data = fin.read()
    # should list all the files...
    for md in tst_file_md_list:
        assert data.find(md["name"]) > 0


def test_metacat_query_q_1(auth, tst_file_md_list, tst_ds):
    with open("qfl1", "w") as qf:
        qf.write(f"files from {tst_ds}")
    with os.popen("metacat query -q qfl1", "r") as fin:
        data = fin.read()
    os.unlink("qfl1")
    for md in tst_file_md_list[:-1]:
        assert data.find(md["name"]) >= 0


def test_metacat_query_q_2(auth, tst_file_md_list, tst_ds):
    with open("qfl1", "w") as qf:
        qf.write(f"files from {tst_ds}")
    with os.popen("metacat query -q qfl1", "r") as fin:
        data = fin.read()
    os.unlink("qfl1")
    for md in tst_file_md_list[:-1]:
        assert data.find(md["name"]) >= 0


def test_metacat_query_mql(auth, tst_file_md_list, tst_ds):
    with os.popen(f"metacat query files from {tst_ds}", "r") as fin:
        data = fin.read()
    for md in tst_file_md_list[:-1]:
        assert data.find(md["name"]) >= 0


def test_metacat_dataset_list(auth, tst_ds):
    with os.popen(f"metacat dataset list {os.environ['USER']}:*", "r") as fin:
        data = fin.read()
    assert data.find(tst_ds) >= 0


def test_metacat_dataset_add_subset(auth, tst_ds):
    tst_ds2 = tst_ds + "_super"
    os.system(f"metacat dataset create {tst_ds2}")
    with os.popen(f"metacat dataset add-subset {tst_ds2} {tst_ds} 2>&1", "r") as fin:
        data = fin.read()
    assert data == ""


def test_metacat_dataset_add_files(auth, tst_ds):
    query = (
        f'(files where creator="{os.environ["USER"]}") - (files from {tst_ds}) limit 10'
    )
    with os.popen(f"metacat dataset add-files --query '{query}' {tst_ds} ", "r") as fin:
        data = fin.read()
    assert data.find("Added 10 files") >= 0


def test_metacat_dataset_update_fail(auth, tst_ds):
    md = '{"foo": "bar"}'
    with os.popen(f"metacat dataset update -j -m '{md}' {tst_ds} 2>&1", "r") as fin:
        data = fin.read()
        # check output
    assert data.find("Metadata parameter without a category") >= 0


def test_metacat_dataset_update(auth, tst_ds):
    md = '{"foo.baz": "bar"}'
    with os.popen(f"metacat dataset update -j -m '{md}' {tst_ds}", "r") as fin:
        data = fin.read()
        # check output
    assert data.find("foo.baz") >= 0
    assert data.find("bar") >= 0


def test_metacat_dataset_remove(auth, tst_ds):
    tst_ds2 = tst_ds + "_super"
    with os.popen(f"metacat dataset remove {tst_ds2}", "r") as fin:
        data = fin.read()
    assert data.strip() == ""
    with os.popen(f"metacat dataset remove {tst_ds2}", "r") as fin:
        data = fin.read()
    assert data.find("not found") >= 0


def test_metacat_namespace_create(auth, tst_ds):
    ns = tst_ds.replace(":", "_")
    with os.popen(f"metacat namespace create -j {ns}", "r") as fin:
        data = fin.read()
        # check output
    print("Got:", data)
    assert data.find('"name":') >= 0
    assert data.find(ns) >= 0


def x_test_metacat_namespace_list(auth):
    ns = tst_ds.replace(":", "_")
    with os.popen("metacat namespace list", "r") as fin:
        data = fin.read()
    assert data.find(ns) >= 0


def test_metacat_namespace_show(auth, tst_ds):
    ns = tst_ds.replace(":", "_")
    with os.popen(f"metacat namespace show {ns}", "r") as fin:
        data = fin.read()
    assert data.find(ns) >= 0


# Categories -- Don't know how to add them, they show up empty
#    in hypot, nothing to test?!?
#
# def x_test_metacat_category_list(auth):
#    with os.popen("metacat category list", "r") as fin:
#        data = fin.read()
#        # check output
#
# def x_test_metacat_category_show(auth):
#    with os.popen("metacat category show", "r") as fin:
#        data = fin.read()
#        # check output
#
def test_metacat_file_declare_sample(auth):
    with os.popen("metacat file declare-sample", "r") as fin:
        data = fin.read()
        # check output
    assert data.find('"namespace":') >= 0
    assert data.find('"name":') >= 0
    assert data.find('"size":') >= 0


# punting
def x_test_metacat_file_move(auth):
    with os.popen("metacat file move", "r") as fin:
        data = fin.read()
        # check output


# deprecated
def x_test_metacat_file_add(auth):
    with os.popen("metacat file add", "r") as fin:
        data = fin.read()
        # check output


def test_metacat_file_datasets(auth, tst_file_md_list, tst_ds):
    ns = tst_file_md_list[0]["namespace"]
    fname = tst_file_md_list[0]["name"]
    with os.popen(f"metacat file datasets {ns}:{fname}", "r") as fin:
        data = fin.read()
    assert data.find(tst_ds) >= 0


def test_metacat_file_update(auth, tst_file_md_list, tst_ds):
    ns = tst_file_md_list[0]["namespace"]
    fname = tst_file_md_list[0]["name"]
    md = '{"foo.bar": "baz"}'
    with os.popen(f"metacat file update -j -m '{md}' {ns}:{fname}", "r") as fin:
        data = fin.read()
    assert data.find("foo.bar") >= 0


def test_metacat_file_update_meta(auth, tst_file_md_list, tst_ds):
    ns = tst_file_md_list[1]["namespace"]
    fname = tst_file_md_list[1]["name"]
    md = '{"foo.bar": "baz"}'
    with os.popen(f"metacat file update-meta -f {ns}:{fname} '{md}'", "r") as fin:
        data = fin.read()
    with os.popen(f"metacat file show -j -m {ns}:{fname}", "r") as fin:
        data2 = fin.read()
    assert data2.find("foo.bar") >= 0


def test_metacat_dataset_remove_files(auth, tst_ds):
    query = f"(files from {tst_ds}) limit 10"
    with os.popen(
        f"metacat dataset remove-files --query '{query}' {tst_ds}", "r"
    ) as fin:
        data = fin.read()
    assert data.find("Removed 10 files") >= 0


def test_metacat_file_retire(auth, tst_file_md_list, tst_ds):
    fname = tst_file_md_list[4]["name"]
    ns = tst_file_md_list[4]["namespace"]
    with os.popen(f"metacat file retire {ns}:{fname}", "r") as fin:
        data = fin.read()
        # check output


def test_metacat_file_name_fid(auth, tst_file_md_list, tst_ds):
    # make sure file name and fid are consistent
    fname = tst_file_md_list[3]["name"]
    ns = tst_file_md_list[3]["namespace"]
    with os.popen(f"metacat file fid {ns}:{fname}", "r") as fin:
        data = fin.read()
        fid = data.strip()
    with os.popen(f"metacat file name --did {fid}", "r") as fin:
        data = fin.read()
        did = data.strip()
    assert f"{ns}:{fname}" == did


def test_metacat_file_show(auth, tst_file_md_list, tst_ds):
    # make sure file name and fid are consistent
    fname = tst_file_md_list[3]["name"]
    ns = tst_file_md_list[3]["namespace"]
    with os.popen(f"metacat file show -j -m {ns}:{fname}", "r") as fin:
        data = fin.read()
    assert data.find(fname) >= 0
    assert data.find(ns) >= 0
    assert json.loads(data)


def test_metacat_validate_good(auth, tst_file_md_list, tst_ds):
    md = tst_file_md_list[0]["metadata"]
    with open("mdf1", "w") as mdf:
        json.dump(md, mdf)
    with os.popen(f"metacat validate mdf1", "r") as fin:
        data = fin.read()
    os.unlink("mdf1")
    assert data.strip() == ""


def test_metacat_validate_bad(auth, tst_file_md_list, tst_ds):
    md = tst_file_md_list[0]["metadata"]
    md["wrong"] = 1
    with open("mdf1", "w") as mdf:
        json.dump(md, mdf)
    with os.popen(f"metacat validate mdf1 2>&1", "r") as fin:
        data = fin.read()
    os.unlink("mdf1")
    assert data.find("wrong") >= 0


def test_metacat_named_query_create(auth, tst_ds):
    nqn = f"{os.environ['USER']}:tst_q_{start_ds}"
    with os.popen(
        f"metacat named_query create {nqn} 'files from {tst_ds}'", "r"
    ) as fin:
        data = fin.read()
        # check output


def test_metacat_named_query_show(auth, tst_ds):
    nqn = f"{os.environ['USER']}:tst_q_{start_ds}"
    with os.popen(f"metacat named_query show {nqn}", "r") as fin:
        data = fin.read()
    assert data.find(f"files from {tst_ds}") >= 0


def test_metacat_named_query_list(auth):
    nqn = f"{os.environ['USER']}:tst_q_{start_ds}"
    with os.popen("metacat named_query list", "r") as fin:
        data = fin.read()
    assert data.find(nqn) >= 0


def test_metacat_named_query_search(auth):
    nqn = f"{os.environ['USER']}:tst_q_{start_ds}"
    with os.popen(
        f"metacat named_query search 'queries matching {nqn[:-2]}*'", "r"
    ) as fin:
        data = fin.read()
    assert data.find(nqn) >= 0
