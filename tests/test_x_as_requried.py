
"""
  Test for new feature --as-required on file creation
"""
import os
import time
import pytest
import json
import time

from env import env, token, auth, start_ds, tst_ds, tst_file_md_list


def test_as_required(auth, tst_ds, tst_file_md_list):
    tst_file_md_list = json.loads(json.dumps(tst_file_md_list))

    for md in tst_file_md_list:
        md["name"] = md["name"] + "_1"
        
    with open("mdf", "w") as mdf:
        json.dump(tst_file_md_list, mdf)

    with os.popen(f"metacat dataset create {tst_ds} ", "r") as fin:
        data = fin.read()

    print("first declare_dataset : got: ", data)

    with os.popen(f"metacat file declare-many mdf {tst_ds}", "r") as fin:
        data = fin.read()

    print("first declare: got: ", data)

    md = tst_file_md_list[0]
    os.popen(f"metacat file retire {md['namespace']}:{md['name']}")

    with os.popen(f"metacat file declare-many --as-required=unretire mdf {tst_ds}", "r") as fin:
        data = fin.read()

    print("second declare: got: ", data)
    os.unlink("mdf")

    assert data.find(os.environ["USER"]) > 0
    for md in tst_file_md_list[1:]:
        assert data.find(md["name"]) > 0
    
