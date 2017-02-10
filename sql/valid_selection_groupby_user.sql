SELECT
  uid,
  student_grade,
  student_class,
  student_number,
  student_name,
  count(cid) AS noc,
  sum(price) AS cost
FROM
  full_selections
WHERE
  total >= lowbound
  AND rank <= upbound
GROUP BY
  uid;
