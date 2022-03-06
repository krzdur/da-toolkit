from da_toolkit.databases import BigQuery
from da_toolkit.experiments import Analysis

import pandas as pd


def test_abtest():
    bq = BigQuery()
    query = '''
                WITH user_stats AS (
                SELECT fullVisitorId,
                       SUM(
                               CASE WHEN hits.eventInfo.eventAction = 'Product Click' THEN 1 END
                           ) prod_clicks,
                       SUM(
                               CASE WHEN hits.eventInfo.eventAction = 'Add to Cart' THEN 1 END
                           ) add_to_cart_clicks,
                FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
                     UNNEST(hits) AS hits
            
                WHERE 1 = 1
                  AND _TABLE_SUFFIX BETWEEN '20170101' AND '20170801'
                  AND hits.eventInfo.eventAction IN ('Product Click', 'Add to Cart')
            
                GROUP BY 1
            )
            
            SELECT CAST(
                           MOD(CAST(fullVisitorId AS NUMERIC), 2)
                       AS INT) AS                variant,
                   COUNT(DISTINCT fullVisitorId) users,
                   COUNT(DISTINCT
                         CASE WHEN prod_clicks > 0 THEN fullVisitorId END
                       )                         users_prod_click,
                   COUNT(DISTINCT
                         CASE WHEN add_to_cart_clicks > 0 THEN fullVisitorId END
                       )                         users_add_to_cart,
                   AVG(prod_clicks)              avg_prod_clicks,
                   AVG(add_to_cart_clicks)       avg_add_to_cart_clicks,
                   VARIANCE(prod_clicks)         var_prod_clicks,
                   VARIANCE(add_to_cart_clicks)  var_add_to_cart_clicks,
            
            FROM user_stats
            GROUP BY 1'''
    df = bq.query(query)
    df['variant'] = df['variant'].astype('str') # variant has to be a string

    abtest = Analysis(df=df, metrics=['users_prod_click'], total_col='users')

    assert abtest.results['users_prod_click']['1']['delta'] == -0.015109790354752684
