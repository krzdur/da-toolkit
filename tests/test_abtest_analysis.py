from da_toolkit.databases import BigQuery
from da_toolkit.experiments import Analysis

import pandas as pd


def test_abtest():
    bq = BigQuery(project='brainly-tutoring')
    query = "SELECT * FROM `brainly-tutoring.experiments.us_and_PlansInMetering` WHERE date = '2021-02-26'"
    df = bq.query(query)

    abtest = Analysis(df=df, metrics=['users_add_answer'])

    expected = {'users_add_answer': {'1': {'cvr': pd.Series([0.016772, 0.016104]),
                                           'delta': -0.039812078502689974,
                                           'z_stat': 0.5881182051793705, 'p_val': 0.2782264771501317,
                                           'power': 0.09048201263909371, 'res': 'not significant'},
                                     '2': {'cvr': pd.Series([0.016772, 0.016754]),
                                           'delta': -0.0010866343969178072,
                                           'z_stat': 0.01588840885943705, 'p_val': 0.49366170861345676,
                                           'power': 0.05002891788921282, 'res': 'not significant'}}
                }

    assert abtest.results['users_add_answer']['2']['delta'] == -0.0010866343969178072
