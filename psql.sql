DROP TABLE IF EXISTS judge_token;
DROP TABLE IF EXISTS map_user_power;
DROP TABLE IF EXISTS map_group_user;
DROP TABLE IF EXISTS map_group_user_power;
DROP TABLE IF EXISTS map_problem_execute;
DROP TABLE IF EXISTS map_contest_problem;
DROP TABLE IF EXISTS map_contest_user;
DROP TABLE IF EXISTS bulletins;
DROP TABLE IF EXISTS wait_submissions;
DROP TABLE IF EXISTS map_submission_testdata;
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS map_verdict_string;
DROP TABLE IF EXISTS contests;
DROP TABLE IF EXISTS testdata;
DROP TABLE IF EXISTS map_problem_tag;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS problems;
DROP TABLE IF EXISTS verdicts;
DROP TABLE IF EXISTS execute_steps;
DROP TABLE IF EXISTS execute_types;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS schools;

CREATE OR REPLACE FUNCTION updated_row() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = date_trunc('second', now());
    RETURN NEW; 
END;
$$ language 'plpgsql';

-- CREATE TABLE table_name (
    --     id              serial          NOT NULL    PRIMARY KEY,
    --     created_at      timestamp       DEFAULT now(),
    --     updated_at      timestamp       DEFAULT now()
    -- );
-- CREATE TRIGGER table_name_updated_at_column BEFORE UPDATE ON table_name FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column_column();

--DROP TABLE IF EXISTS users;
CREATE TABLE schools(
    id              serial          NOT NULL    PRIMARY KEY,
    name            varchar(255)    NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER schools_update_row BEFORE UPDATE ON schools FOR EACH ROW EXECUTE PROCEDURE updated_row();
INSERT INTO schools (name) VALUES('NCTU');

CREATE TABLE users (
    id              serial          NOT NULL    PRIMARY KEY,
    account         varchar(32)     NOT NULL,
    passwd          varchar(32)     NOT NULL,
    email           varchar(255)    NOT NULL,
    name            varchar(32)     DEFAULT '',
    student_id      varchar(32)     DEFAULT '',
    school_id       integer         DEFAULT 1   REFERENCES schools(id)  ON DELETE CASCADE,
    token           varchar(64)     NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second', now()),
    updated_at      timestamp       DEFAULT date_trunc('second', now())
);
CREATE TRIGGER users_updated_row BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE UNIQUE INDEX on users (token);
CREATE UNIQUE INDEX on users (account);
CREATE INDEX on users (name);
CREATE INDEX on users (student_id);
INSERT INTO users (account, passwd, email, student_id, school_id, token) VALUES ('admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@gmail.com', '0000000', '1', 'P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr');
INSERT INTO users (account, passwd, email, student_id, school_id, token) VALUES ('user', 'ee11cbb19052e40b07aac0ca060c23ee', 'user@gmail.com', '0000001', '1', 'TOKEN@user@a35668De30ED26b0cff046EBFD108964');
INSERT INTO users (account, passwd, email, student_id, school_id, token) VALUES ('test', '098f6bcd4621d373cade4e832627b4f6', 'test@gmail.com', '0000002', '1', 'NCTUOJ@6766394053819075738@Ec77c214D7cE6ad1a543D93B5786a290');

--DROP TABLE IF EXISTS map_user_power;
CREATE TABLE map_user_power (
    id              serial          NOT NULL    PRIMARY KEY,
    user_id         integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    power           integer         NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_user_power_updated_row BEFORE UPDATE ON map_user_power FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_user_power (power);
CREATE INDEX ON map_user_power (user_id);
INSERT INTO map_user_power (user_id, power) VALUES (1, 1);
INSERT INTO map_user_power (user_id, power) VALUES (1, 2);
INSERT INTO map_user_power (user_id, power) VALUES (1, 3);
INSERT INTO map_user_power (user_id, power) VALUES (1, 4);

--DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
    id              serial          NOT NULL    PRIMARY KEY,
    name            varchar(255)    NOT NULL,
	type			integer			NOT NULL DEFAULT 0,
    description     varchar(255)    NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER groups_updated_row BEFORE UPDATE ON groups FOR EACH ROW EXECUTE PROCEDURE updated_row();
INSERT INTO groups (name, description) VALUES ('Group1', 'For Group1');
INSERT INTO groups (name, description) VALUES ('Group2', 'For Group2');
INSERT INTO groups (name, description) VALUES ('Group3', 'For Group3');

--DROP TABLE IF EXISTS map_group_user;
CREATE TABLE map_group_user (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL    REFERENCES groups(id)   ON DELETE CASCADE,
    user_id         integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    priority        integer         NOt NULL    DEFAULT 999,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE INDEX on map_group_user (group_id);
CREATE INDEX on map_group_user (user_id);
CREATE UNIQUE INDEX ON map_group_user(group_id, user_id);
CREATE TRIGGER map_group_user_updated_row BEFORE UPDATE ON map_group_user FOR EACH ROW EXECUTE PROCEDURE updated_row();
--INSERT INTO map_group_user (group_id, user_id) VALUES (1, 0);
INSERT INTO map_group_user (group_id, user_id) VALUES (1, 1);
INSERT INTO map_group_user (group_id, user_id) VALUES (2, 1);
INSERT INTO map_group_user (group_id, user_id) VALUES (1, 2);
INSERT INTO map_group_user (group_id, user_id) VALUES (2, 2);

--DROP TABLE IF EXISTS map_group_user_power;
CREATE TABLE map_group_user_power (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL    REFERENCES groups(id)   ON DELETE CASCADE,
    user_id         integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    power           integer         NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_group_user_power_updated_row BEFORE UPDATE ON map_group_user_power FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_group_user_power (group_id);
CREATE INDEX ON map_group_user_power (user_id);
CREATE INDEX ON map_group_user_power (power);
CREATE UNIQUE INDEX ON map_group_user_power (group_id, user_id, power);
INSERT INTO map_group_user_power (group_id, user_id, power) VALUES (1, 1, 1);
INSERT INTO map_group_user_power (group_id, user_id, power) VALUES (1, 1, 2);
INSERT INTO map_group_user_power (group_id, user_id, power) VALUES (1, 1, 3);
INSERT INTO map_group_user_power (group_id, user_id, power) VALUES (1, 1, 4);
INSERT INTO map_group_user_power (group_id, user_id, power) VALUES (1, 1, 5);

--DROP TABLE IF EXISTS bulletins;
CREATE TABLE bulletins (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL    REFERENCES groups(id)   ON DELETE CASCADE,
    setter_user_id  integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    title           varchar(255)    DEFAULT '',
    content         text            DEFAULT '',
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER bulletins_updated_row BEFORE UPDATE ON bulletins FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON bulletins (group_id);
INSERT INTO bulletins (group_id, setter_user_id, title, content) VALUES (1, 1, 'Public', 'New Group Public');
INSERT INTO bulletins (group_id, setter_user_id, title, content) VALUES (2, 1, 'Normal', 'New Group Normal');

--DROP TABLE IF EXISTS execute_types;
CREATE TABLE execute_types (
    id              serial          NOT NULL    PRIMARY KEY,
    description     varchar(255)    NOT NULL    DEFAULT '',
    lang            integer         NOT NULL,
    recompile       integer         NOT NULL    DEFAULT 0   CHECK(recompile = ANY('{0,1}')), 
    setter_user_id  integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    priority        integer         NOT NULL    DEFAULT 999,
	cm_mode			varchar(255)	DEFAULT '',
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER execute_types_updated_row BEFORE UPDATE ON execute_types FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX on execute_types (priority);
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic C', 0, 1, 1, 'text/x-csrc');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic C++', 1, 1, 2, 'text/x-c++src');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic C++11', 1, 1, 3, 'text/x-c++src');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic Java', 2, 1, 4, 'text/x-java');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic Python2', 3, 1, 5, 'text/x-python');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic Python3', 4, 1, 6, 'text/x-python');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic Go', 5, 1, 7, 'text/x-go');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic Perl', 6, 1, 8, 'text/x-perl');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic Javascript', 7, 1, 9, 'text/javascript');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic Ruby', 9, 1, 10, 'text/x-ruby');
INSERT INTO execute_types (description, lang, setter_user_id, priority, cm_mode) values ('Basic shell', 10, 1, 11, 'text/x-sh');
--map_lang = {
--0: "C",
--1: "C++",
--2: "Java",
--3: "Python2",
--4: "Python3",
--5: "Go",
--6: "Perl",
--7: "Javascript",
--8: "Haskell",
--9: "ruby",
--10:"sh",
--}


--DROP TABLE IF EXISTS execute_steps;
CREATE TABLE execute_steps (
    id              serial          NOT NULL    PRIMARY KEY,
    execute_type_id integer         NOT NULL    REFERENCES execute_types(id)    ON DELETE CASCADE,
    command         varchar(255)    NOT NULL    DEFAULT '',
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER execute_steps_updated_row BEFORE UPDATE ON execute_steps FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON execute_steps (execute_type_id);
INSERT INTO execute_steps (execute_type_id, command) values (1, 'gcc __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (1, './a.out');
INSERT INTO execute_steps (execute_type_id, command) values (2, 'g++ __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (2, './a.out');
INSERT INTO execute_steps (execute_type_id, command) values (3, 'g++ -std=c++11  __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (3, './a.out');
INSERT INTO execute_steps (execute_type_id, command) values (4, 'javac __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (4, 'java -Xmx__MEMORY_LIMIT__k -Xss8m __MAIN_FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (5, 'python2 -m py_compile __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (5, 'python2 __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (6, 'python3 -m py_compile __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (6, 'python3 __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (7, 'TMPDIR="." go build -o a.out __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (7, './a.out');
INSERT INTO execute_steps (execute_type_id, command) values (8, 'perl __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (9, 'd8 __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (10, 'ruby __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (11, 'sh __FILE__');


--INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic C', 0, 1, 1);
--INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic C++', 1, 1, 2);
--INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic C++11', 1, 1, 3);
--INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic Java', 2, 1, 4);
--INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic Python2', 3, 1, 5);
--INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic Python3', 4, 1, 6);
--INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic Go', 5, 1, 7);

--DROP TABLE IF EXISTS verdicts;
CREATE TABLE verdicts(
    id              serial          NOT NULL    PRIMARY KEY,
    title           varchar(255)    ,
    execute_type_id integer         NOT NULL    DEFAULT 0   REFERENCES execute_types(id)    ON DELETE CASCADE,
    problem_id      integer         NOT NULL    DEFAULT 0,
    file_name       varchar(255)    NOT NULL,
    setter_user_id  integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER verdicts_update_row BEFORE UPDATE ON verdicts FOR EACH ROW EXECUTE PROCEDURE updated_row();
INSERT INTO verdicts (title, execute_type_id, file_name, setter_user_id) VALUES ('Token By Character(Ignore Lines)', 2, 'main.cpp', 1);

--DROP TABLE IF EXISTS problems;
CREATE TABLE problems (
    id              serial          NOT NULL    PRIMARY KEY,
    title           varchar(255)    NOT NULL DEFAULT '',
    pdf             boolean         NOT NULL DEFAULT FALSE,
    description     text            NOT NULL DEFAULT '',
    input           text            NOT NULL DEFAULT '',
    output          text            NOT NULL DEFAULT '',
    sample_input    text            NOT NULL DEFAULT '',
    sample_output   text            NOT NULL DEFAULT '',
    hint            text            NOT NULL DEFAULT '',
    source          text            NOT NULL DEFAULT '',
    group_id        integer         NOT NULL    REFERENCES groups(id)   ON DELETE CASCADE,
    setter_user_id  integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    visible         integer         NOT NULL DEFAULT 0 CHECK (visible = ANY('{0, 1}')),
    interactive     integer         NOT NULL DEFAULT 0 CHECK (interactive = ANY('{0, 1}')),
    verdict_id      integer         DEFAULT 1   REFERENCES verdicts(id) ON DELETE CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
ALTER SEQUENCE problems_id_seq RESTART WITH 10001;
CREATE TRIGGER problems_updated_row BEFORE UPDATE ON problems FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON problems (visible);
CREATE INDEX ON problems (group_id);
INSERT INTO problems (group_id, setter_user_id, visible) values (1, 1, 0);
INSERT INTO problems (group_id, setter_user_id, visible) values (1, 1, 1);
INSERT INTO problems (group_id, setter_user_id, visible) values (2, 1, 0);
INSERT INTO problems (group_id, setter_user_id, visible) values (2, 1, 1);
INSERT INTO problems (group_id, setter_user_id, visible) values (3, 1, 0);
INSERT INTO problems (group_id, setter_user_id, visible) values (3, 1, 1);

--DROP TABLE IF EXISTS map_problem_execute;
CREATE TABLE map_problem_execute (
    id              serial          NOT NULL    PRIMARY KEY,
    problem_id      integer         NOT NULL    REFERENCES problems(id) ON DELETE CASCADE,
    execute_type_id integer         NOT NULL    REFERENCES execute_types(id)    ON DELETE CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_problem_execute_updated_row BEFORE UPDATE ON map_problem_execute FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_problem_execute (problem_id);
CREATE INDEX ON map_problem_execute (execute_type_id);
CREATE UNIQUE INDEX ON map_problem_execute (problem_id, execute_type_id);
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



--DROP TABLE IF EXISTS testdata;
CREATE TABLE testdata(
    id              serial          NOT NULL    PRIMARY KEY,
    problem_id      integer         NOT NULL    REFERENCES problems(id) ON DELETE CASCADE,
    time_limit      integer         NOT NULL    DEFAULT 1000,
    memory_limit    integer         NOT NULL    DEFAULT 262144,
    output_limit    integer         NOT NULL    DEFAULT 64,
    score           integer         NOT NULL    DEFAULT 0,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER testdata_updated_row BEFORE UPDATE ON testdata FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON testdata (problem_id);

CREATE TABLE map_verdict_string (
    id              serial          NOT NULL    PRIMARY KEY,
    abbreviation    varchar(15)     NOT NULL,
    description     varchar(31)     NOT NULL,
    priority        integer         NOT NULL,
    color           varchar(32)     NOT NULL    DEFAULT '#000',
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_verdict_string_updated_row BEFORE UPDATE ON map_verdict_string FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_verdict_string(priority);
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('Pending', 'In Queue', 1, '#000');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('SE', 'System Error', 2, '#000');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('CE', 'Compile Error', 3, 'rgb(51, 122, 183)');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('RE', 'Runtime Error', 4, 'rgb(163, 188, 0)');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('MLE', 'Memory Limit Exceed', 5, '#000');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('TLE', 'Time Limit Exceed', 6, 'rgb(156, 39, 176)');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('OLE', 'Output Limit Exceed', 7, '#000');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('WA', 'Wrong Answer', 8, 'rgb(244, 67, 54)');
INSERT INTO map_verdict_string (abbreviation,description,priority,color) VALUES('AC', 'Accepted', 9, 'rgb(76, 175, 80)');


--DROP TABLE IF EXISTS submissions;
CREATE TABLE submissions(
    id              serial          NOT NULL    PRIMARY KEY,
    user_id         integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    problem_id      integer         NOT NULL    REFERENCES problems(id) ON DELETE CASCADE,
    execute_type_id integer         NOT NULL    REFERENCES execute_types(id)    ON DELETE CASCADE,
    time_usage      integer         ,
    memory_usage    integer         ,
    verdict         integer         NOT NULL    DEFAULT 1   REFERENCES map_verdict_string(id)   ON DELETE CASCADE,
    score           integer         ,
    length          integer         NOT NULL,
    file_name       varchar(255)    NOT NULL,
    ip              inet            NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
ALTER SEQUENCE submissions_id_seq RESTART WITH 10001;
CREATE TRIGGER submissions_updated_row BEFORE UPDATE ON submissions FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON submissions (user_id);
CREATE INDEX ON submissions (problem_id);
CREATE INDEX ON submissions (execute_type_id);
CREATE INDEX ON submissions (memory_usage);
CREATE INDEX ON submissions (time_usage);
CREATE INDEX ON submissions (verdict);
CREATE INDEX ON submissions (length);
CREATE INDEX ON submissions (created_at);

CREATE TABLE map_submission_testdata (
    id              serial          NOT NULL    PRIMARY KEY,
    testdata_id     integer         NOT NULL    REFERENCES testdata(id)     ON DELETE CASCADE,
    submission_id   integer         NOT NULL    REFERENCES submissions(id)  ON DELETE CASCADE,
    time_usage      integer,
    memory_usage    integer,
    score           integer,
    verdict         integer         DEFAULT 1   REFERENCES map_verdict_string(id)   ON DELETE CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_submission_testdata_updated_row BEFORE UPDATE ON map_submission_testdata FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_submission_testdata(submission_id);
CREATE INDEX ON map_submission_testdata(time_usage);
CREATE INDEX ON map_submission_testdata(memory_usage);
CREATE INDEX ON map_submission_testdata(verdict);

--DROP TABLE IF EXISTS contests;
CREATE TABLE contests(
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL    REFERENCES groups(id)   ON DELETE CASCADE,
    visible         integer         NOT NULL    DEFAULT 0 CHECK (visible = ANY('{0, 1}')),
    setter_user_id  integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    title           varchar(255)    ,
    description     text            ,
    register_start  timestamp       NOT NULL    DEFAULT date_trunc('second', now()),
    register_end    timestamp       NOT NULL    DEFAULT date_trunc('second', now()),
    "start"         timestamp       NOT NULL    DEFAULT date_trunc('second', now()),
    "freeze"        integer         NOT NULL    DEFAULT 0 CHECK ("freeze" * interval '1 minute' <= "end"-"start"),
    "end"           timestamp       NOT NULL    DEFAULT date_trunc('second', now()),
    "type"          integer         NOT NULL    DEFAULT 0,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
ALTER SEQUENCE contests_id_seq RESTART WITH 1001;
CREATE TRIGGER contests_update_row BEFORE UPDATE ON contests FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON contests (group_id);
CREATE INDEX ON contests (visible);
INSERT INTO contests (group_id, setter_user_id, title, description) values (1, 1, 'test', 'contest');

--DROP TABLE IF EXISTS map_contest_problem;
CREATE TABLE map_contest_problem (
    id              serial          NOT NULL    PRIMARY KEY,
    contest_id      integer         NOT NULL    REFERENCES contests(id) ON DELETE CASCADE,
    problem_id      integer         NOT NULL    REFERENCES problems(id) ON DELETE CASCADE,
    score           varchar(255)    NOT NULL    DEFAULT '',
    penalty         integer         NOT NULL    DEFAULT 20,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_conteset_problem_update_row BEFORE UPDATE ON map_contest_problem FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_contest_problem (contest_id);
CREATE INDEX ON map_contest_problem (problem_id);
CREATE UNIQUE INDEX ON map_contest_problem (contest_id, problem_id);
INSERT INTO map_contest_problem (contest_id, problem_id) VALUES (1001, 10001);

--DROP TABLE IF EXISTS map_contest_user;
CREATE TABLE map_contest_user (
    id              serial          NOT NULL    PRIMARY KEY,
    user_id         integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    contest_id      integer         NOT NULL    REFERENCES contests(id) ON DELETE CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_contest_user_update_row BEFORE UPDATE ON map_contest_user FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE UNIQUE INDEX ON map_contest_user (user_id, contest_id);
CREATE INDEX ON map_contest_user (user_id);
CREATE INDEX ON map_contest_user (contest_id);
INSERT INTO map_contest_user (user_id, contest_id) VALUES(1, 1001);

CREATE TABLE wait_submissions (
    id              serial          NOT NULL    PRIMARY KEY,
    submission_id   integer         NOT NULL    REFERENCES submissions(id)  ON  DELETE  CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER wait_submissions_update_row BEFORE UPDATE ON wait_submissions FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE UNIQUE INDEX ON wait_submissions(submission_id);

CREATE TABLE tags (
    id              serial          NOT NULL     PRIMARY KEY,
    tag             varchar(31)     NOT NULL,
    description     varchar(255)    DEFAULT '',
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER tags_update_row BEFORE UPDATE ON tags FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON tags(tag);
INSERT INTO tags (tag) VALUES('DP');
INSERT INTO tags (tag) VALUES('String');

CREATE TABLE map_problem_tag (
    id              serial          NOT NULL        PRIMARY KEY,
    problem_id      integer         NOT NULL        REFERENCES problems(id)     ON DELETE CASCADE,
    tag_id          integer         NOT NULL        REFERENCES tags(id)         ON DELETE CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_problem_tag_update_row BEFORE UPDATE ON map_problem_tag FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_problem_tag (problem_id);
CREATE INDEX ON map_problem_tag (tag_id);
CREATE UNIQUE INDEX ON map_problem_tag (problem_id,tag_id);

CREATE TABLE judge_token (
    id              serial          NOT NULL    PRIMARY KEY,
    addr            varchar(31)     DEFAULT '',
    description     varchar(255)    DEFAULT '',
    token           varchar(255)    NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER judge_token_update_row BEFORE UPDATE ON judge_token FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE UNIQUE INDEX ON judge_token(token);
INSERT INTO judge_token (token) VALUES('TOKEN');
