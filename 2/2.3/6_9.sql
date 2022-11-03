ALTER TABLE IF EXISTS public.employees
    ADD COLUMN year_bonus numeric DEFAULT 0;

UPDATE public.employees as e
SET year_bonus = (
SELECT SUM(CASE
				WHEN S.SCORE = 'A' THEN 0.2
				WHEN S.SCORE = 'B' THEN 0.1
				WHEN S.SCORE = 'C' THEN 0
				WHEN S.SCORE = 'D' THEN -0.1
				WHEN S.SCORE = 'E' THEN -0.2
				ELSE 0.0
	END)
FROM PUBLIC.SCORES AS S
WHERE EMPLOYEE_ID = e.id
	AND date > NOW()::date - interval '1 Year'
);
	
SELECT *
FROM PUBLIC.EMPLOYEES;