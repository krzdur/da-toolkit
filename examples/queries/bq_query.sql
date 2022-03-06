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
  AND _TABLE_SUFFIX BETWEEN '20170101' AND '20170101'
      AND hits.eventInfo.eventAction IN ('Product Click', 'Add to Cart')

GROUP BY 1
LIMIT 10