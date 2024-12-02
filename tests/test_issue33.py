"""
  This file has a commandline based integration tests for the metacat
  client and server for issue#33 about reparenting

  This suite needs to be run in-order, later tests depend on earlier ones. 
"""
import os
import time
import pytest
import json
import time

from env import env, token, auth, start_ds, tst_ds, tst_file_md_list

@pytest.fixture
def tst_ds_33(tst_ds):
    # a fresh dataset, our generic one with _33 on the end
    return tst_ds + "_33"

@pytest.fixture
def tst_file_md_list_33(tst_file_md_list):
    # a fresh metadata list with files with _33 in them and 
    # the fifth one being descended from the first two
    mdl = tst_file_md_list[:5].copy()
    for md in mdl:
        md["name"] = md["name"].replace(".txt","_33.txt")
    mdl[4]["parents"] = [{"namespace":x['namespace'], "name":x['name']} for x in mdl[:2]]
    yield mdl

#
# Setup for the real test ; these are clones of the tests in
# test_commandline with the alternate namespace,file metadata
#
def test_metacat_dataset_create_33(auth, tst_ds_33):
    with os.popen(f"metacat dataset create {tst_ds_33} ", "r") as fin:
        data = fin.read()
    assert data.find(tst_ds_33) > 0
    assert data.find("ataset") > 0
    assert data.find("eated") > 0  # dont fail if they fix spelling of cteated


def test_metacat_file_declare_many_33(auth, tst_ds_33, tst_file_md_list_33):
    with open("mdf", "w") as mdf:
        json.dump(tst_file_md_list_33[:4], mdf)
    with os.popen(f"metacat file declare-many mdf {tst_ds_33}", "r") as fin:
        data = fin.read()
    print(f"got: {data}")
    for md in tst_file_md_list_33[:4]:
        assert data.find(md["name"]) > 0
    with open("mdf", "w") as mdf:
        json.dump(tst_file_md_list_33[4:], mdf)
    with os.popen(f"metacat file declare-many mdf {tst_ds_33}", "r") as fin:
        data = fin.read()
    os.unlink("mdf")
    print(f"got: {data}")
    assert data.find(os.environ["USER"]) > 0
    for md in tst_file_md_list_33[5:]:
        assert data.find(md["name"]) > 0

    ns = tst_file_md_list_33[0]["namespace"]
    fn = tst_file_md_list_33[4]["name"]
    cmd = f"metacat file  show -jml {ns}:{fn}"
    print(f"running: {cmd}")
    with(os.popen(cmd , "r")) as fin:
        data=fin.read()
    print(f"got: {data}")
    
    # check response for requested parents
    assert data.find(tst_file_md_list_33[0]["name"]) > 0
    assert data.find(tst_file_md_list_33[1]["name"]) > 0
    # also check issue #60
    assert data.find('"created_timestamp"') > 0
    assert data.find('"created_timestamp": null') < 0


def test_update_33(auth, tst_ds_33, tst_file_md_list_33):
    ns = tst_file_md_list_33[0]["namespace"]
    n1 = tst_file_md_list_33[2]["name"]
    n2 = tst_file_md_list_33[3]["name"]
    fn = tst_file_md_list_33[4]["name"]
    cmd = f"metacat file update {ns}:{fn} --replace --parents {ns}:{n1},{ns}:{n2}"
    print(f"running: {cmd}")
    with(os.popen(cmd , "r")) as fin:
        data=fin.read()
    print(f"got: {data}")

    cmd = f"metacat file  show -jml {ns}:{fn}"
    print(f"running: {cmd}")
    with(os.popen(cmd , "r")) as fin:
        data=fin.read()
    print(f"got: {data}")
    
    # check response for new parents
    assert data.find(n1) > 0
    assert data.find(n2) > 0

