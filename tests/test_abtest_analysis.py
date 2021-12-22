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


def test_mean_test():
    bq = BigQuery(project='brainly-tutoring')
    query = "SELECT * FROM `brainly-tutoring.experiments.us_web_TutorVerified1day`"
    df = bq.query(query)

    abtest = Analysis(df=df, metrics=['avg_number_of_answers_prime'], variances=['var_number_of_answers_prime'],
                      variant_col='experimentVariant', total_col='user_counter', kind='mean')

    expected = {'avg_number_of_answers_prime': {'1': {'mean': [0.018830508032320635, 0.02033743020622658],
                                                      'delta': 0.08002557187089532,
                                                      't_stat': -0.8430733578842278, 'p_val': 0.39918829209893414,
                                                      # 'power': 0.09048201263909371,
                                                      'res': 'not significant'},
                                                '2': {'cvr': [0.018830508032320635, 0.017353844007255488],
                                                      'delta': -0.07841870344287072,
                                                      't_stat': 0.824308933091005, 'p_val': 0.4097649002298738,
                                                      # 'power': 0.05002891788921282,
                                                      'res': 'not significant'}}
                }

    assert abtest.results['avg_number_of_answers_prime']['2']['delta'] == -0.07841870344287072
