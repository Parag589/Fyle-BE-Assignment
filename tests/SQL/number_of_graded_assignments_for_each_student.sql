SELECT student_id, COUNT(*) AS num_submitted_assignments
FROM assignments
WHERE state = 'GRADED'
GROUP BY student_id;
