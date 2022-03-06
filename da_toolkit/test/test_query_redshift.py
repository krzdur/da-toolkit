from da_toolkit.databases import Redshift
import os


def test_access_rds():
    rd = Redshift()
    assert rd.engine.url.database == os.getenv('RDS_NAME')