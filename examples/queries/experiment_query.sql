SELECT CAST(
               MOD(CAST(fullVisitorId AS NUMERIC), 2)
               AS INT) as                 variant, # as there were no experiments run on the sample data, we're mocking it
       COUNT(DISTINCT fullVisitorId) users,
       COUNT(DISTINCTa
             CASE WHEN hits.eventInfo.eventAction = 'Product Click' THEN fullVisitorId END
           )                         users_prod_click,
       COUNT(DISTINCT
             CASE WHEN hits.eventInfo.eventAction = 'Add to Cart' THEN fullVisitorId END
           )                         users_add_to_cart,

FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
     UNNEST(hits) AS hits

WHERE 1 = 1
  AND _TABLE_SUFFIX BETWEEN '20170101' AND '20170801'

GROUP BY 1