from da_toolkit.databases import Redshift


def test_access_rds():
    rd = Redshift('datastudio', 'Jusdh^&#fghd$%273_).,aL*(!@')
    assert rd.login == 'datastudio'

def test_query_rds():
    rd = Redshift('tableau', 'nlzs48$ssf^uiUhwv.')
    query = '''SELECT COUNT(DISTINCT question_id)
                FROM public.bi_questions
                WHERE date_created::DATE = '2021-02-01\''''
    df = rd.query(query=query)
    assert df.iloc[0, 0] == 316963
