
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

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id              serial          NOT NULL    PRIMARY KEY,
    account         varchar(32)     NOT NULL,
    passwd          varchar(32)     NOT NULL,
    email           varchar(255)    NOT NULL,
    student_id      varchar(255)    NOT NULL,
    school_id       integer         NOT NULL,
    token           varchar(64)     NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second', now()),
    updated_at      timestamp       DEFAULT date_trunc('second', now())
);
CREATE TRIGGER users_updated_row BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE UNIQUE INDEX on users (token);
INSERT INTO users (account, passwd, email, student_id, school_id, token) VALUES ('admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@gmail.com', '0000000', '0', 'P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr');


DROP TABLE IF EXISTS map_user_power;
CREATE TABLE map_user_power (
    id              serial          NOT NULL    PRIMARY KEY,
    user_id         integer         NOT NULL,
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

DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
    id              serial          NOT NULL    PRIMARY KEY,
    name            varchar(255)    NOT NULL,
    description     varchar(255)    NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER groups_updated_row BEFORE UPDATE ON groups FOR EACH ROW EXECUTE PROCEDURE updated_row();
INSERT INTO groups (name, description) VALUES ('Public', 'For Public');
INSERT INTO groups (name, description) VALUES ('Normal', 'For Normal');

DROP TABLE IF EXISTS map_group_user;
CREATE TABLE map_group_user (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL,
    user_id         integer         NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_group_user_updated_row BEFORE UPDATE ON map_group_user FOR EACH ROW EXECUTE PROCEDURE updated_row();
INSERT INTO map_group_user (group_id, user_id) VALUES (1, 0);
INSERT INTO map_group_user (group_id, user_id) VALUES (1, 1);
INSERT INTO map_group_user (group_id, user_id) VALUES (2, 1);

DROP TABLE IF EXISTS map_group_user_power;
CREATE TABLE map_group_user_power (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL,
    user_id         integer         NOT NULL,
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

DROP TABLE IF EXISTS bulletins;
CREATE TABLE bulletins (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL,
    setter_user_id  integer         NOT NULL,
    title           varchar(255)    DEFAULT '',
    content         text            DEFAULT '',
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER bulletins_updated_row BEFORE UPDATE ON bulletins FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON bulletins (group_id);
INSERT INTO bulletins (group_id, setter_user_id, title, content) VALUES (1, 1, 'Public', 'New Group Public');
INSERT INTO bulletins (group_id, setter_user_id, title, content) VALUES (2, 1, 'Normal', 'New Group Normal');


DROP TABLE IF EXISTS problems;
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
    group_id        integer         NOT NULL,
    setter_user_id  integer         NOT NULL,
    visible         integer         NOT NULL DEFAULT 0,
    interactive     integer         NOT NULL DEFAULT 0,
    verdict_id      integer         DEFAULT 1,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
ALTER SEQUENCE problems_id_seq RESTART WITH 10001;
CREATE TRIGGER problems_updated_row BEFORE UPDATE ON problems FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON problems (visible);
CREATE INDEX ON problems (group_id);
INSERT INTO problems (group_id, setter_user_id) values (1, 1);
INSERT INTO problems (group_id, setter_user_id) values (2, 1);

DROP TABLE IF EXISTS execute_types;
CREATE TABLE execute_types (
    id              serial          NOT NULL    PRIMARY KEY,
    description     varchar(255)    NOT NULL    DEFAULT '',
    lang            integer         NOT NULL,
    setter_user_id  integer         NOT NULL,
    priority        integer         NOT NULL    DEFAULT 999,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER execute_types_updated_row BEFORE UPDATE ON execute_types FOR EACH ROW EXECUTE PROCEDURE updated_row();
INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic C', 0, 1, 1);
INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic C++', 1, 1, 3);
INSERT INTO execute_types (description, lang, setter_user_id, priority) values ('Basic C++14', 1, 1, 2);

DROP TABLE IF EXISTS execute_steps;
CREATE TABLE execute_steps (
    id              serial          NOT NULL    PRIMARY KEY,
    execute_type_id integer         NOT NULL,
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

DROP TABLE IF EXISTS map_problem_execute;
CREATE TABLE map_problem_execute (
    id              serial          NOT NULL    PRIMARY KEY,
    problem_id      integer         NOT NULL,
    execute_type_id integer         NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_problem_execute_updated_row BEFORE UPDATE ON map_problem_execute FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_problem_execute (problem_id);
CREATE INDEX ON map_problem_execute (execute_type_id);
CREATE UNIQUE INDEX ON map_problem_execute (problem_id, execute_type_id);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (1, 1);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (1, 2);
INSERT INTO map_problem_execute(problem_id, execute_type_id) VALUES (1, 3);

DROP TABLE IF EXISTS testdata;
CREATE TABLE testdata(
    id              serial          NOT NULL    PRIMARY KEY,
    problem_id      integer         NOT NULL,
    time_limit      integer         NOT NULL    DEFAULT 1000,
    memory_limit    integer         NOT NULL    DEFAULT 65536,
    output_limit    integer         NOT NULL    DEFAULT 65536,
    score           integer         NOT NULL    DEFAULT 0,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER testdata_updated_row BEFORE UPDATE ON testdata FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON testdata (problem_id);
INSERT INTO testdata (problem_id, score) values (1, 50);
INSERT INTO testdata (problem_id, score) values (1, 50);

DROP TABLE IF EXISTS submissions;
CREATE TABLE submissions(
    id              serial          NOT NULL    PRIMARY KEY,
    user_id         integer         NOT NULL,
    problem_id      integer         NOT NULL,
    execute_type_id integer         NOT NULL,
    time_usage      integer         ,
    memory_usage    integer         ,
    verdict         integer         NOT NULL    DEFAULT 0,
    score           integer         ,
    length          integer         NOT NULL,
    file_name       varchar(255)    NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER submissions_updated_row BEFORE UPDATE ON submissions FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON submissions (user_id);
CREATE INDEX ON submissions (problem_id);
CREATE INDEX ON submissions (execute_type_id);
CREATE INDEX ON submissions (memory_usage);
CREATE INDEX ON submissions (time_usage);
CREATE INDEX ON submissions (verdict);
CREATE INDEX ON submissions (length);
INSERT INTO submissions (user_id, problem_id, execute_type_id, length, file_name) VALUES (1, 1, 1, 100, 'xd.cpp');


DROP TABLE IF EXISTS verdicts;
CREATE TABLE verdicts(
    id              serial          NOT NULL    PRIMARY KEY,
    execute_type_id integer         NOT NULL    DEFAULT 0,
    file_name       varchar(255)    NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER verdicts_update_row BEFORE UPDATE ON verdicts FOR EACH ROW EXECUTE PROCEDURE updated_row();

DROP TABLE IF EXISTS contests;
CREATE TABLE contests(
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL,
    visible         integer         NOT NULL,
    setter_user_id  integer         NOT NULL,
    title           varchar(255)    ,
    description     text            ,
    register_start  timestamp       NOT NULL    DEFAULT date_trunc('second', now()),
    register_end    timestamp       NOT NULL    DEFAULT date_trunc('second', now()),
    "start"         timestamp       NOT NULL    DEFAULT date_trunc('second', now()),
    "end"           timestamp       NOT NULL    DEFAULT date_trunc('second', now()),
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER contests_update_row BEFORE UPDATE ON contests FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON contests (group_id);

DROP TABLE IF EXISTS map_user_contest;
CREATE TABLE map_user_contest (
    id              serial          NOT NULL    PRIMARY KEY,
    user_id         integer         NOT NULL,
    contest_id      integer         NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER map_user_contest_update_row BEFORE UPDATE ON map_user_contest FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON map_user_contest (user_id);
CREATE INDEX ON map_user_contest (contest_id);

