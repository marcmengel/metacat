import os
import pytest

@pytest.fixture
def env():
    os.environ['METACAT_AUTH_SERVER_URL'] = 'https://metacat.fnal.gov:8143/auth/hypot_dev'
    os.environ['DATA_DISPATCHER_URL'] = 'https://metacat.fnal.gov:9443/hypot_dd/data'
    os.environ['METACAT_SERVER_URL'] = 'https://metacat.fnal.gov:9443/hypot_meta_dev/app'
    os.environ['DATA_DISPATCHER_AUTH_URL'] = 'https://metacat.fnal.gov:8143/auth/hypot_dev'
    os.environ['BEARER_TOKEN_FILE'] = '/tmp/bt_mc_test%d' % os.getpid()

@pytest.fixture
def token(env):
    os.system("htgettoken -i hypot -a htvaultprod.fnal.gov")

