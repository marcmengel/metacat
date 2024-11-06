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

from env import env,token,auth, tst_ds

def test_metacat_query_explain_57(auth, tst_ds):
    with os.popen(f"metacat query --explain files from {tst_ds}", "r") as fin:
        data = fin.read()
    print(f"got: {data}")
    assert data.find(tst_ds) > 0
    assert data.find("select") >= 0
