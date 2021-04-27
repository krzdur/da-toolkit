from da_toolkit.databases import Redshift


def test_access_rds():
    rd = Redshift()
    assert rd.login == 'tableau'

def test_query_rds():
    rd = Redshift()
    query = '''SELECT COUNT(DISTINCT question_id)
                FROM public.bi_questions
                WHERE date_created::DATE = '2021-02-01\''''
    df = rd.query(query=query)
    assert df.iloc[0, 0] == 316963
