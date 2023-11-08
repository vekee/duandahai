SELECT 
      T1.student_id AS studentId
    , T1.name AS name
    , SUM(T2.score AS score) AS totalScore
FROM 
    student T1,
    score T2
WHERE 
        T1.student_id = T2.student_id
    AND T1.gender = 'male'
GROUP BY 
      T1.student_id
    , T1.name




SELECT 
      T1.age AS age
    , T1.name AS name
    , T1.student_id AS studentId
FROM 
    student T1 
WHERE 
        T1.gender = 'male'
    AND T1.age > '18'
ORDER BY 
      T1.age DESC
    , T1.name ASC




SELECT 
      T1.student_id AS studentId
    , T1.name AS name
    , T2.course_name AS courseName
    , T2.score AS score
FROM 
    student T1
LEFT OUTER JOIN 
    optional_course T2
ON 
        T1.student_id = T2.student_id
    AND T2.course_name = 'computer',
    ( SELECT 
              T31.XX
            , T31.yy
      FROM 
          sub_table_xx T31,
          sub_table_yy T32
      WHERE 
          T31.id = T32.id
    ) T3
WHERE 
        T1.xx = T3.xx
    AND T1.name = 'Jack'





SELECT 
      T1.student_id AS studentId
    , T1.name AS name
    , T2.course_name AS courseName
    , T2.score AS score
FROM 
    student T1
LEFT OUTER JOIN 
    optional_course T2
ON 
        T1.student_id = T2.student_id
    AND T2.course_name = 'computer'
WHERE 
    T1.name = 'Jack'








SELECT 
      T1.name AS name
    , T1.student_id AS studentId
FROM 
    student T1 
WHERE 
    T1.name = 'Jack'










