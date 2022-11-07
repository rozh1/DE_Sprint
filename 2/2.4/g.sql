ALTER TABLE IF EXISTS public.employees
    ADD COLUMN salary_old numeric;

UPDATE public.employees as e
SET salary_old = salary;

UPDATE public.employees as e
SET salary = 
 (CASE
				WHEN year_bonus >= 0.2 THEN 1.2 * salary_old
				WHEN year_bonus < 0.2 and year_bonus >= 0 THEN 1.1 * salary_old
				ELSE salary_old
	END);
	
SELECT *
FROM PUBLIC.EMPLOYEES;