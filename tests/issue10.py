import os
import time
import pytest
import json

from env import env, token, auth


def test_issue_10(auth):
    # use case from issue 10
    start_ts = int(time.time())
    user = os.environ["USER"]
    os.system(f"""
        set -x
        metacat dataset create {user}:steve_test_retire_{start_ts}
        metacat file declare {user}:1mbtestfile.st2024{start_ts} {user}:steve_test_retire_{start_ts} -s 1024000 -c adler32:a0e10001
        metacat file declare {user}:1mbtestfile.st2024{start_ts}.child {user}:steve_test_retire_{start_ts} -s 1024000 -c adler32:a0e10001 --parents {user}:1mbtestfile.st2024{start_ts}
        metacat file declare {user}:1mbtestfile.st2024{start_ts}.child2 {user}:steve_test_retire_{start_ts} -s 1024000 -c adler32:a0e10001 --parents {user}:1mbtestfile.st2024{start_ts}
        metacat dataset files {user}:steve_test_retire_{start_ts}
        metacat file show {user}:1mbtestfile.st2024{start_ts} -l
        metacat file show {user}:1mbtestfile.st2024{start_ts}.child -l
        metacat file show {user}:1mbtestfile.st2024{start_ts}.child2 -l
    """)

    with os.popen(f"""
        set -x
        metacat query children '(files from {user}:steve_test_retire_{start_ts})'
        metacat query parents ' (files from {user}:steve_test_retire_{start_ts})'
    """) as fin:
         out1 = fin.read()

    os.system(f"""
        set -x
        metacat file retire {user}:1mbtestfile.st2024{start_ts}.child
    """)

    with os.popen(f"""
        set -x
        metacat query children '(files from {user}:steve_test_retire_{start_ts})'
        metacat query parents ' (files from {user}:steve_test_retire_{start_ts})'
    """) as fin:
         out2 = fin.read()
    
    # Make sure our file is in the pre-remove query  but  not the post remove...
    assert(out1.find( f"{user}:1mbtestfile.st2024{start_ts}.child") >= 0)
    assert(out2.find( f"{user}:1mbtestfile.st2024{start_ts}.child") < 0)
