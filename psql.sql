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
DROP TABLE IF EXISTS contests;
DROP TABLE IF EXISTS testdata;
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
    student_id      varchar(32)     NOT NULL,
    school_id       integer         NOT NULL    REFERENCES schools(id)  ON DELETE CASCADE,
    token           varchar(64)     NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second', now()),
    updated_at      timestamp       DEFAULT date_trunc('second', now())
);
CREATE TRIGGER users_updated_row BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE UNIQUE INDEX on users (token);
CREATE UNIQUE INDEX on users (account);
CREATE UNIQUE INDEX on users (student_id);
INSERT INTO users (account, passwd, email, student_id, school_id, token) VALUES ('admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@gmail.com', '0000000', '1', 'P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr');
INSERT INTO users (account, passwd, email, student_id, school_id, token) VALUES ('user', 'ee11cbb19052e40b07aac0ca060c23ee', 'user@gmail.com', '0000001', '1', 'TOKEN@user@a35668De30ED26b0cff046EBFD108964');


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
    description     varchar(255)    NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER groups_updated_row BEFORE UPDATE ON groups FOR EACH ROW EXECUTE PROCEDURE updated_row();
INSERT INTO groups (name, description) VALUES ('Group1', 'For Group1');
INSERT INTO groups (name, description) VALUES ('Group2', 'For Group2');

--DROP TABLE IF EXISTS map_group_user;
CREATE TABLE map_group_user (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL    REFERENCES groups(id)   ON DELETE CASCADE,
    user_id         integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE INDEX on map_group_user (group_id);
CREATE INDEX on map_group_user (user_id);
CREATE TRIGGER map_group_user_updated_row BEFORE UPDATE ON map_group_user FOR EACH ROW EXECUTE PROCEDURE updated_row();
--INSERT INTO map_group_user (group_id, user_id) VALUES (1, 0);
INSERT INTO map_group_user (group_id, user_id) VALUES (1, 1);
INSERT INTO map_group_user (group_id, user_id) VALUES (2, 1);
INSERT INTO map_group_user (group_id, user_id) VALUES (1, 2);

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
    setter_user_id  integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    priority        integer         NOT NULL    DEFAULT 999,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER execute_types_updated_row BEFORE UPDATE ON execute_types FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX on execute_types (priority);
INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic C', 0, 1, 1);
INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic C++', 1, 1, 3);
INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic C++14', 1, 1, 2);

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
INSERT INTO execute_steps (execute_type_id, command) values (1, '__CHECK_CE__ ./a.out');
INSERT INTO execute_steps (execute_type_id, command) values (1, './a.out');
INSERT INTO execute_steps (execute_type_id, command) values (2, 'g++ __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (2, '__CHECK_CE__ ./a.out');
INSERT INTO execute_steps (execute_type_id, command) values (2, './a.out');
INSERT INTO execute_steps (execute_type_id, command) values (3, 'g++ -std=c++11  __FILE__');
INSERT INTO execute_steps (execute_type_id, command) values (3, '__CHECK_CE__ ./a.out');
INSERT INTO execute_steps (execute_type_id, command) values (3, './a.out');

--DROP TABLE IF EXISTS verdicts;
CREATE TABLE verdicts(
    id              serial          NOT NULL    PRIMARY KEY,
    title           varchar(255)    ,
    execute_type_id integer         NOT NULL    DEFAULT 0   REFERENCES execute_types(id)    ON DELETE CASCADE,
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
    title           varchar(255)    ,
    description     text            ,
    input           text            ,
    output          text            ,
    sample_input    text            ,
    sample_output   text            ,
    hint            text            ,
    source          text            ,
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
INSERT INTO problems (group_id, setter_user_id) values (1, 1);
INSERT INTO problems (group_id, setter_user_id) values (2, 1);

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



--DROP TABLE IF EXISTS testdata;
CREATE TABLE testdata(
    id              serial          NOT NULL    PRIMARY KEY,
    problem_id      integer         NOT NULL    REFERENCES problems(id) ON DELETE CASCADE,
    time_limit      integer         NOT NULL    DEFAULT 1000,
    memory_limit    integer         NOT NULL    DEFAULT 65536,
    output_limit    integer         NOT NULL    DEFAULT 65536,
    score           integer         NOT NULL    DEFAULT 0,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER testdata_updated_row BEFORE UPDATE ON testdata FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON testdata (problem_id);
INSERT INTO testdata (problem_id, score) values (10001, 50);
INSERT INTO testdata (problem_id, score) values (10001, 50);

CREATE TABLE map_verdict_string (
    id              serial          NOT NULL    PRIMARY KEY,
    abbreviation    varchar(15)     NOT NULL,
    description     varchar(31)     NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_verdict_testdata_updated_row BEFORE UPDATE ON map_verdict_testdata FOR EACH ROW EXECUTE PROCEDURE updated_row();
INSERT INTO map_verdict_string (abbreviation,description) VALUES('Pending', 'In Queue');
INSERT INTO map_verdict_string (abbreviation,description) VALUES('SE', 'System Error');
INSERT INTO map_verdict_string (abbreviation,description) VALUES('RE', 'Runtime Error');
INSERT INTO map_verdict_string (abbreviation,description) VALUES('MLE', 'Memory Limit Exceed');
INSERT INTO map_verdict_string (abbreviation,description) VALUES('TLE', 'Time Limit Exceed');
INSERT INTO map_verdict_string (abbreviation,description) VALUES('WA', 'Wrong Answer');
INSERT INTO map_verdict_string (abbreviation,description) VALUES('AC', 'Accepted');


--DROP TABLE IF EXISTS submissions;
CREATE TABLE submissions(
    id              serial          NOT NULL    PRIMARY KEY,
    user_id         integer         NOT NULL    REFERENCES users(id)    ON DELETE CASCADE,
    problem_id      integer         NOT NULL    REFERENCES problems(id) ON DELETE CASCADE,
    execute_type_id integer         NOT NULL    REFERENCES execute_types(id)    ON DELETE CASCADE,
    time_usage      integer         ,
    memory_usage    integer         ,
    verdict         integer         NOT NULL    DEFAULT 7   REFERENCES map_verdict_string(id)   ON DELETE CASCADE,
    score           integer         ,
    length          integer         NOT NULL,
    file_name       varchar(255)    NOT NULL,
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
INSERT INTO submissions (user_id, problem_id, execute_type_id, length, file_name) VALUES (1, 10001, 1, 100, 'xd.cpp');

CREATE TABLE map_submission_testdata (
    id              serial          NOT NULL    PRIMARY KEY,
    submission_id   integer         NOT NULL    REFERENCES submissions(id)  ON DELETE CASCADE,
    time            integer         DEFAULT 0,
    memory          integer         DEFAULT 0,
    verdict         integer         DEFAULT 7   REFERENCES map_verdict_string(id)   ON DELETE CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_submission_testdata_updated_row BEFORE UPDATE ON map_submission_testdata FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_submission_testdata(submission_id);
CREATE INDEX ON map_submission_testdata(time);
CREATE INDEX ON map_submission_testdata(memory);
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
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_conteset_problem_update_row BEFORE UPDATE ON map_contest_problem FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_contest_problem (contest_id);
CREATE INDEX ON map_contest_problem (problem_id);
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
CREATE INDEX ON map_contest_user (user_id);
CREATE INDEX ON map_contest_user (contest_id);

CREATE TABLE wait_submissions (
    id              serial          NOT NULL    PRIMARY KEY,
    submission_id   integer         NOT NULL    REFERENCES submissions(id)  ON  DELETE  CASCADE,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER wait_submissions_update_row BEFORE UPDATE ON wait_submissions FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE UNIQUE INDEX ON wait_submissions(submission_id);

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
