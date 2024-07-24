
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

def test_metacat_dataset_create(auth, tst_ds):
    tst_ds =  tst_ds + "_cksum"
    with os.popen(f"metacat dataset create {tst_ds} ", "r") as fin:
        data = fin.read()
    assert data.find(tst_ds) > 0
    assert data.find("ataset") > 0
    assert data.find("eated") > 0  # dont fail if they fix spelling of cteated

def test_metacat_file_declare_bad_chksum_1(auth, tst_file_md_list, tst_ds):
    # add a file we did before, with ck1 on the filename, and
    # a 4-char adler32 checksum -- this should fail due to the checksum
    # being short.
    tst_ds =  tst_ds + "_cksum"
    md = tst_file_md_list[0].copy()
    md["name"] = "ck1_" + md["name"]
    md["checksums"]["adler32"] = md["checksums"]["adler32"][:4]
    print("metadata:\n", json.dumps(md))
    with open("mdf1", "w") as mdf:
        json.dump(md, mdf)
    with os.popen(f"metacat file declare -f mdf1 {tst_ds} 2>&1", "r") as fin:
        data = fin.read()
    print(f"got data: '{data}'")
    os.unlink("mdf1")
    assert data.find("validation error") > 0
    assert data.find("adler32: value is wrong length ") > 0

def test_metacat_file_declare_bad_chksum_2(auth, tst_file_md_list, tst_ds):
    # add a file we did before, with ck1 on the filename, and
    # a funky adler32 checksum, should report bad digits
    tst_ds =  tst_ds + "_cksum"
    md = tst_file_md_list[0].copy()
    md["name"] = "ck1_" + md["name"]
    md["checksums"]["adler32"] = "xy123456"
    print("metadata:\n", json.dumps(md))
    with open("mdf1", "w") as mdf:
        json.dump(md, mdf)
    with os.popen(f"metacat file declare -f mdf1 {tst_ds} 2>&1", "r") as fin:
        data = fin.read()
    print(f"got data: '{data}'")
    os.unlink("mdf1")
    assert data.find("validation error") > 0
    assert data.find("invalid digit") > 0

