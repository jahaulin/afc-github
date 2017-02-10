SELECT
  count(distinct cid) AS courses,  -- 有開課的課程總數
  count(cid) AS noc,               -- 所有選課次數
  count(distinct uid) AS users,    -- 所有選到課的人數
  count(uid) AS nou,               -- 所有選課人次
  sum(price) AS cost               -- 總收費
FROM
  full_selections
WHERE
  total >= lowbound
  AND rank <= upbound;
;
