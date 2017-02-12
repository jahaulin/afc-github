.shell echo "--- 各班級選課統計 ---"
SELECT
  student_grade,
  student_class,
  count(cid),
  sum(price)
FROM
  full_selections
WHERE
  total >= lowbound
  AND rank <= upbound
GROUP BY
  student_grade,
  student_class
ORDER BY
  student_grade,
  student_class;

.shell echo "--- 各年級選課統計 ---"
SELECT
  student_grade,
  count(cid),
  sum(price)
FROM
  full_selections
WHERE
  total >= lowbound
  AND rank <= upbound
GROUP BY
  student_grade
ORDER BY
  student_grade;
