%%bigquery --project brainly-bi df_raw
-- Query V2.1 (27.10.2020 - Positive John)

SELECT
 -- Dimensions
  exp.experimentVariant                                                   AS experimentVariant,
  device.deviceCategory                                                   AS deviceType,
 # (SELECT value from hits.customDimensions where index = 2)               AS loggedStatus,
 # CASE WHEN totals.newVisits = 1 THEN 'New Visitor' ELSE 'Returning Visitor' END  AS userType,

 -- Totals
  COUNT(DISTINCT fullVisitorId)                                           AS uniqueUsers,
  COUNT(CASE WHEN hits.type = 'PAGE' THEN hits.page.pagePath END)         AS totalPageviews,
  COUNT(DISTINCT
      CASE WHEN totals.bounces = 1
      THEN CONCAT(fullVisitorId, CAST(visitId AS STRING)
      ) END)                                                              AS bounces,
  COUNT(DISTINCT
      CONCAT(fullVisitorId, CAST(visitId AS STRING)))                     AS sessions,
  COUNT(CASE WHEN hits.eventInfo.eventAction = "user read an answer"
  THEN hits.eventInfo.eventAction END)                                                      AS totalAnswersRead,
  COUNT(CASE WHEN hits.eventInfo.eventAction = "watch video ad click"
  THEN hits.eventInfo.eventAction END)                                                      AS totalVideoViews,
    COUNT(CASE WHEN hits.eventInfo.eventAction = "user visited an answered question"
  THEN hits.eventInfo.eventAction END)                                                      AS totalAnsweredQuestionsView,


 -- 1. users: eventAction=read an answer
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'user read an answer'
       THEN fullVisitorId END
       ) AS users_who_read_an_answer,

 -- 2. users: eventAction=create account
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'create account'
       THEN fullVisitorId END
       ) AS users_who_created_new_account,

 -- 3. users: eventAction=log in
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'log in'
       THEN fullVisitorId END
       ) AS users_who_login,

 -- 4. users: eventAction=confirmation trial|confirmation payment
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'confirmation trial'
      OR hits.eventInfo.eventAction = 'confirmation payment success'
      THEN fullVisitorId END
       ) AS users_who_subscribe,

 -- 5. users: eventAction=answer question
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'answer question'
       THEN fullVisitorId END
       ) AS users_who_answer,

 -- 6. users: eventAction=ask question
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'ask question'
       THEN fullVisitorId END
       ) AS users_who_ask,

 -- 7. users: eventAction=search results show
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'search results show'
       THEN fullVisitorId END
       ) AS users_who_search,

 -- 8. users: eventAction=rate answer
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'rate answer'
       THEN fullVisitorId END
       ) AS users_who_rate_answer,

-- 9. users: eventAction=thank answer
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'thank answer'
       THEN fullVisitorId END
       ) AS users_who_thank_answer,

-- 10. users: eventAction=user visited an answered question
    COUNT(DISTINCT
      CASE WHEN hits.eventInfo.eventAction = 'user visited an answered question'
       THEN fullVisitorId END
       ) AS users_who_visit_answered_question,

-- Change the code number before ga_sessions to the right market where the experiment is running
FROM  `brainly-bi.67275862.ga_sessions_*`, UNNEST(hits) as hits, UNNEST(hits.experiment) AS exp

WHERE
-- Add your time frame of analysis below
   _TABLE_SUFFIX BETWEEN '20201022' AND '20201029'

-- Add the experimentID from google optimize that is under production
   AND exp.experimentId = "3zGsIRTtT3O3yjTbHW1eVA"

-- Are you analysing one platform only? Add the filter below!
   #AND device.deviceCategory = "mobile"

-- Exclude webcache (This is a common issue in the US market)
   AND NOT REGEXP_CONTAINS(hits.page.hostname, 'webcache.googleusercontent.com')

GROUP BY
1,2#,3

ORDER BY
1