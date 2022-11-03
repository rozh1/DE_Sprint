CREATE TABLE departments
(
    id serial NOT NULL,
    name character varying NOT NULL,
    supervisor character varying,
    employee_count integer NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE employees
(
    id serial NOT NULL,
    name character varying,
    birthday date,
    employed_date date,
    "position" character varying,
    postion_level character varying,
    salary numeric,
    department_id integer NOT NULL,
    has_permission boolean DEFAULT false,
    PRIMARY KEY (id),
    FOREIGN KEY (department_id) REFERENCES public.departments (id) ON UPDATE NO ACTION ON DELETE SET NULL,
    CONSTRAINT employee_level CHECK (postion_level IN ('jun','middle','senior','lead') OR postion_level = NULL)
);


CREATE TABLE scores
(
    employee_id integer NOT NULL,
    date date NOT NULL,
    score character(1) DEFAULT 'E',
    PRIMARY KEY (date, employee_id),
    CONSTRAINT score_check CHECK (score IN ('A','B','C','D','E'))
);

CREATE OR REPLACE FUNCTION update_departmet_employee_count()
    RETURNS trigger
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
   CASE TG_OP
   WHEN 'INSERT' THEN
      UPDATE departments AS d
      SET    employee_count = employee_count + 1
      WHERE  d.id = NEW.department_id;
   WHEN 'DELETE' THEN
      UPDATE departments AS d
      SET    employee_count = employee_count - 1 
      WHERE  d.id = OLD.department_id;
   END CASE;
   
   RETURN NULL;   
END
$BODY$;

CREATE TRIGGER employee_department_trigger
    AFTER INSERT OR DELETE
    ON public.employees
    FOR EACH ROW
    EXECUTE FUNCTION public.update_departmet_employee_count();

INSERT INTO departments(name, supervisor) VALUES 
('Бухгалтерский', 'Андреева А. Д.'),
('IT отдел', 'Тихомиров П. А.');


INSERT INTO employees(name, birthday, employed_date, "position", postion_level, salary, department_id, has_permission) VALUES 
('Харитонов Я. М.', '1992-05-21', '2010-01-07','Разработчик','lead',125000,2,true),
('Самсонов М. А.', '1999-05-21', '2020-01-07','Разработчик','jun',40000,2,true),
('Грачева А. П.', '1999-05-21', '2021-05-07','QA-инженер','middle',85000,2,true),
('Терехов Э. Д.', '1990-05-21', '2018-09-01','Разработчик','senior',250000,2,true),
('Власова В. Р.', '1992-12-21', '2010-01-07','Главный бухгалтер',NULL,60000,1,true),
('Шестакова М. С.', '1996-08-25', '2020-03-01','бухгалтер',NULL,45000,1,true);


INSERT INTO scores(employee_id, date, score) VALUES 
(1, '2021-12-25', 'A'),
(1, '2022-03-25', 'B'),
(1, '2022-06-25', 'A'),
(1, '2022-09-25', 'B'),
(2, '2021-12-25', 'B'),
(2, '2022-03-25', 'C'),
(2, '2022-06-25', 'D'),
(2, '2022-09-25', 'C'),
(3, '2021-12-25', 'B'),
(3, '2022-03-25', 'A'),
(3, '2022-06-25', 'A'),
(3, '2022-09-25', 'B'),
(4, '2021-12-25', 'A'),
(4, '2022-03-25', 'A'),
(4, '2022-06-25', 'A'),
(4, '2022-09-25', 'A'),
(5, '2021-12-25', 'A'),
(5, '2022-03-25', 'C'),
(5, '2022-06-25', 'A'),
(5, '2022-09-25', 'A'),
(6, '2021-12-25', 'B'),
(6, '2022-03-25', 'B'),
(6, '2022-06-25', 'A'),
(6, '2022-09-25', 'A');