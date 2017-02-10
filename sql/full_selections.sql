.headers on
.mode csv
--
-- DROP
--
DROP TABLE full_selections;

--
-- CREATE
--
CREATE TABLE full_selections AS
SELECT
  s.*, -- 選課
  c.*, -- 課程
  u.*  -- 使用者
FROM
  (
    SELECT
      *,
      /* 產生選課序位 */
      (
        SELECT
          count()+ 1
        FROM
          (
            SELECT
              *
            FROM
              selection AS u
            WHERE
              u.sid < t.sid
              AND u.course_id = t.course_id
          )
      ) AS rank,
      /* 產生總選課人數 */
      (
        SELECT
          count()
        FROM
          selection u
        WHERE
          u.course_id = t.course_id
        GROUP BY
          course_id
      ) AS total
    FROM
      selection t
    ORDER BY
      t.course_id
  ) AS s,
  USER AS u,
  course AS c
WHERE
  s.user_id = u.uid
  AND s.course_id = c.cid
ORDER BY
  s.sid;

---
--- SELECT
---
SELECT
  *
FROM
  full_selections
ORDER BY
  course_id;
