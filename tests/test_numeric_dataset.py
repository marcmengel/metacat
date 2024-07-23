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


# test having a dataset start with a number, add a file to it,
# and query it

def test_metacat_numeric_dataset_create(auth, tst_ds):
    tst_ds = tst_ds.replace(":",":2")
    with os.popen(f"metacat dataset create {tst_ds} ", "r") as fin:
        data = fin.read()
    assert data.find(tst_ds) > 0
    assert data.find("ataset") > 0
    assert data.find("eated") > 0  # dont fail if they fix spelling of cteated

def test_metacat_numeric_ds_declare(auth, tst_file_md_list, tst_ds):
    tst_ds = tst_ds.replace(":",":2")
    md = tst_file_md_list[0].copy()
    md["name"] = md["name"] + "x"
    with open("mdfn", "w") as mdf:
        json.dump(md, mdf)
    with os.popen(f"metacat file declare -f mdfn {tst_ds} ", "r") as fin:
        data = fin.read()
    print(f"got data: '{data}'")
    os.unlink("mdfn")
    assert data.find(os.environ["USER"]) > 0
    assert data.find(md["name"]) > 0

def test_metacat_numeric_query_q(auth, tst_file_md_list, tst_ds):
    tst_ds = tst_ds.replace(":",":2")
    md = tst_file_md_list[0].copy()
    md["name"] = md["name"] + "x"
    with open("qfl1", "w") as qf:
        qf.write(f"files from {tst_ds}")
    with os.popen("metacat query -q qfl1", "r") as fin:
        data = fin.read()
    os.unlink("qfl1")
    assert data.find(md["name"]) >= 0
