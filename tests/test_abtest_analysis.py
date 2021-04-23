from da_toolkit.databases import BigQuery
from da_toolkit.experiments import Analysis

import pandas as pd


def test_abtest():
    bq = BigQuery(project='brainly-tutoring')
    query = "SELECT * FROM `brainly-tutoring.experiments.us_and_PlansInMetering` WHERE date = '2021-02-26'"
    df = bq.query(query)

    abtest = Analysis(df=df, metrics=['users_add_answer', 'bplus_subs', 'tutoring_subs'])

    expected = {'users_add_answer': {'1': {'cvr': pd.Series([0.016754, 0.016772]),
                                           'delta': 0.0010878164556960002,
                                           'z_stat': -0.01588840885943705, 'p_val': 0.49366170861345676,
                                           'power': 0.05002891788921282, 'res': 'not significant'},
                                     '2': {'cvr': pd.Series([0.016754, 0.016104]),
                                                'delta': -0.03876757028112454,
                                           'z_stat': 0.569717130803695, 'p_val': 0.2844347846008663,
                                           'power': 0.08793795112260097, 'res': 'not significant'}},
                'bplus_subs': {'1': {'cvr': pd.Series([0.008216, 0.006725]),
                                             'delta': -0.1815005274261603,
                                     'z_stat': 1.9390955376704726, 'p_val': 0.026244852985232704,
                                     'power': 0.49234126622066765, 'res': 'significant!'},
                               '2': {'cvr': pd.Series([0.008216, 0.008032]),
                                            'delta': -0.022363965666588048,
                                     'z_stat': 0.22822903596804692, 'p_val': 0.4097340948001864,
                                     'power': 0.05598825141282003, 'res': 'not significant'}},
                'tutoring_subs': {'1': {'cvr': pd.Series([0.002900, 0.002848]),
                                               'delta': -0.017800632911392444,
                                        'z_stat': 0.10792244583138043, 'p_val': 0.4570286059561353,
                                        'power': 0.05133520043379809, 'res': 'not significant'},
                                  '2': {'cvr': pd.Series([0.002900, 0.002892]),
                                               'delta': -0.0028112449799196915,
                                        'z_stat': 0.016915737949897956, 'p_val': 0.4932519187475877,
                                        'power': 0.050032778263321226, 'res': 'not significant'}}}

    assert abtest.results['users_add_answer']['2']['delta'] == -0.03876757028112454
