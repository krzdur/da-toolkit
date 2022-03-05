from da_toolkit.databases import BigQuery


def test_access_bq():
    bq = BigQuery()

def test_query_bq():
    bq = BigQuery('brainly-tutoring')
    query = 'SELECT * FROM `brainly-bi.da_recruitment.trial_conversions` LIMIT 1'
    df = bq.query(query=query)
    assert df['user_pseudo_id'][0] == '94f3a9ec84240b0a9b5061656abe78dc'