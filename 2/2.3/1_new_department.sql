
INSERT INTO departments(name, supervisor) VALUES 
('отдел Интеллектуального анализа данных', 'Потапов Д. Ф.');


INSERT INTO employees(name, birthday, employed_date, "position", postion_level, salary, department_id, has_permission) VALUES 
('Исаева Т. А.', '1997-01-29', '2022-06-07','ML-инженер','middle',130000,3,true),
('Еремин А. П.', '1993-05-21', '2022-06-18','Дата-инженер','middle',130000,3,true);


INSERT INTO scores(employee_id, date, score) VALUES 
(7, '2022-06-25', 'A'),
(7, '2022-09-25', 'B'),
(8, '2022-06-25', 'A'),
(8, '2022-09-25', 'A');