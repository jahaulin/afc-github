SELECT 
  cid, 
  total, 
  lowbound, 
  rank, 
  total, 
  student_grade, 
  student_class, 
  student_number, 
  student_name, 
  price 
FROM 
  full_selections 
WHERE 
  total >= lowbound 
  AND rank <= upbound 
ORDER BY 
  cid;
