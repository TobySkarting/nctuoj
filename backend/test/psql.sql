INSERT INTO users (account, passwd, email, student_id, school_id, token) VALUES ('user', 'ee11cbb19052e40b07aac0ca060c23ee', 'user@gmail.com', '0000001', '1', 'TOKEN@user@a35668De30ED26b0cff046EBFD108964');
INSERT INTO users (account, passwd, email, student_id, school_id, token) VALUES ('test', '098f6bcd4621d373cade4e832627b4f6', 'test@gmail.com', '0000002', '1', 'NCTUOJ@6766394053819075738@Ec77c214D7cE6ad1a543D93B5786a290');

INSERT INTO groups (name, description) VALUES ('Group2', 'For Group2');
INSERT INTO groups (name, description) VALUES ('Group3', 'For Group3');

INSERT INTO map_group_user (group_id, user_id) VALUES (2, 1);
INSERT INTO map_group_user (group_id, user_id) VALUES (1, 2);
INSERT INTO map_group_user (group_id, user_id) VALUES (2, 2);

INSERT INTO bulletins (group_id, setter_user_id, title, content) VALUES (2, 1, 'Normal', 'New Group Normal');
INSERT INTO bulletins (group_id, setter_user_id, title, content) VALUES (3, 1, 'Normal 2', 'New Group Normal 2');

INSERT INTO verdicts (title, execute_type_id, file_name, setter_user_id) VALUES ('Token By Character(Ignore Lines)', 2, 'main.cpp', 1);

INSERT INTO problems (group_id, setter_user_id, visible) values (1, 1, 0);
INSERT INTO problems (group_id, setter_user_id, visible) values (1, 1, 1);
INSERT INTO problems (group_id, setter_user_id, visible) values (2, 1, 0);
INSERT INTO problems (group_id, setter_user_id, visible) values (2, 1, 1);
INSERT INTO problems (group_id, setter_user_id, visible) values (3, 1, 0);
INSERT INTO problems (group_id, setter_user_id, visible) values (3, 1, 1);

INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 1);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 2);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 3);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 4);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 5);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 6);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 8);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 9);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 10);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10001, 11);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 1);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 2);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 3);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 4);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 5);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 6);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 8);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 9);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 10);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10002, 11);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 1);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 2);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 3);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 4);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 5);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 6);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 8);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 9);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 10);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10003, 11);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 1);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 2);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 3);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 4);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 5);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 6);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 8);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 9);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 10);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10004, 11);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 1);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 2);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 3);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 4);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 5);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 6);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 8);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 9);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 10);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10005, 11);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 1);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 2);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 3);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 4);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 5);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 6);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 8);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 9);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 10);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (10006, 11);

INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('Pending', 'In Queue', 1, '#000');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('SE', 'System Error', 2, '#000');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('CE', 'Compile Error', 3, 'rgb(51, 122, 183)');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('RE', 'Runtime Error', 4, 'rgb(163, 188, 0)');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('MLE', 'Memory Limit Exceed', 5, '#000');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('TLE', 'Time Limit Exceed', 6, 'rgb(156, 39, 176)');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('OLE', 'Output Limit Exceed', 7, '#000');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('WA', 'Wrong Answer', 8, 'rgb(244, 67, 54)');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('AC', 'Accepted', 9, 'rgb(76, 175, 80)');

INSERT INTO tags (tag) VALUES('DP');
INSERT INTO tags (tag) VALUES('String');

