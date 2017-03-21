.mode csv

SELECT
  student_grade,
  student_class,
  student_number,
  student_name,
  count(cid) AS noc,
  sum(price) AS cost,
  rtrim(group_concat(name||price||x'0d'||x'0a', ""),x'0d'||x'0a')
FROM
  full_selections
WHERE
  total >= lowbound
  AND rank <= upbound
GROUP BY
  uid
ORDER BY
  student_grade,
  student_class,
  student_number
;
