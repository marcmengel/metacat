import os
import time
import pytest
import json

from env import env, token, auth


def test_issue_10_1(auth):
    # use case from issue 10
    start_ts = int(time.time())
    user = os.environ["USER"]
    os.system(f"""
        set -x
        metacat dataset create {user}:steve_test_retire_{start_ts}
        metacat file declare {user}:1mbtestfile.st2024{start_ts} {user}:steve_test_retire_{start_ts} -s 1024000 -c adler32:a0e10001
        metacat file declare {user}:1mbtestfile.st2024{start_ts}.child1 {user}:steve_test_retire_{start_ts} -s 1024000 -c adler32:a0e10001 --parents {user}:1mbtestfile.st2024{start_ts}
        metacat file declare {user}:1mbtestfile.st2024{start_ts}.child2 {user}:steve_test_retire_{start_ts} -s 1024000 -c adler32:a0e10001 --parents {user}:1mbtestfile.st2024{start_ts}
        metacat dataset files {user}:steve_test_retire_{start_ts}
        metacat file show {user}:1mbtestfile.st2024{start_ts} -l
        metacat file show {user}:1mbtestfile.st2024{start_ts}.child1 -l
        metacat file show {user}:1mbtestfile.st2024{start_ts}.child2 -l
    """)

    with os.popen(f"""
        set -x
        metacat query children '(files from {user}:steve_test_retire_{start_ts})'
    """) as fin:
         out1 = fin.read()

    os.system(f"""
        set -x
        metacat file retire {user}:1mbtestfile.st2024{start_ts}.child1
    """)

    with os.popen(f"""
        set -x
        metacat query children '(files from {user}:steve_test_retire_{start_ts})'
    """) as fin:
         out2 = fin.read()
    
    # Make sure our file is in the pre-remove query  but  not the post remove...
    print(f"comparing: '{out1}' '{out2}'")
    assert(out1.find( f"{user}:1mbtestfile.st2024{start_ts}.child1") >= 0)
    assert(out2.find( f"{user}:1mbtestfile.st2024{start_ts}.child1") < 0)

def test_issue_10_2(auth):
    # make sure we don't barf on updated/retired queries
    with os.popen(f"""
 metacat query 'files where updated_by == {os.environ['USER']} and updated_timestamp > now 
       and retired_by == {os.environ['USER']} and retired_timestamp > now and retired == false'
    """) as fin:
         out = fin.read()
    assert(out.strip() == "")
