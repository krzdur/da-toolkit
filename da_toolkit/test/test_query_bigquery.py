from da_toolkit.databases import BigQuery


def test_access_bq():
    bq = BigQuery()

def test_query_bq():
    bq = BigQuery()
    query = '''SELECT COUNT(DISTINCT fullVisitorId) users FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`'''
    df = bq.query(query=query)
    assert df['users'][0] == 2293
