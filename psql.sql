CREATE OR REPLACE FUNCTION update_modified_column() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified = now();
    RETURN NEW; 
END;
$$ language 'plpgsql';

CREATE TABLE table_name (
    id              serial          NOT NULL    PRIMARY KEY,
    created_at      timestamp       DEFAULT now(),
    updated_at      timestamp       DEFAULT now()
);
CREATE TRIGGER table_name_modified BEFORE UPDATE ON table_name FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TABLE users (
    id              serial          NOT NULL    PRIMARY KEY,
    account         varchar(32)     NOT NULL,
    passwd          varchar(32)     NOT NULL,
    email           varchar(255)    NOT NULL,
    student_id      varchar(255)    NOT NULL,
    school_id       integer         NOT NULL,
    created_at      timestamp       DEFAULT now(),
    updated_at      timestamp       DEFAULT now()
);
CREATE TRIGGER users_modified BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TABLE map_user_power (
    id              serial          NOT NULL    PRIMARY KEY,
    user_id         integer         NOT NULL,
    power           integer         NOT NULL,
    created_at      timestamp       DEFAULT now(),
    updated_at      timestamp       DEFAULT now()
);
CREATE TRIGGER map_user_power_modified BEFORE UPDATE ON map_user_power FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE INDEX ON map_user_power (power);
CREATE INDEX ON map_user_power (user_id);
INSERT INTO map_user_power (user_id, power) VALUES (1, 1);

CREATE TABLE groups (
    id              serial          NOT NULL    PRIMARY KEY,
    name            varchar(255)    NOT NULL,
    description     varchar(255)    NOT NULL,
    created_at      timestamp       DEFAULT now(),
    updated_at      timestamp       DEFAULT now()
);
CREATE TRIGGER groups_modified BEFORE UPDATE ON groups FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
INSERT INTO groups (name, description) VALUES ('Public', 'For Public');

CREATE TABLE map_group_user (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL,
    user_id         integer         NOT NULL,
    created_at      timestamp       DEFAULT now(),
    updated_at      timestamp       DEFAULT now()
);
CREATE TRIGGER map_group_user_modified BEFORE UPDATE ON map_group_user FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
INSERT INTO map_group_user (group_id, user_id) VALUES (1, 1);

CREATE TABLE map_group_user_power (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL,
    user_id         integer         NOT NULL,
    power           integer         NOT NULL,
    created_at      timestamp       DEFAULT now(),
    updated_at      timestamp       DEFAULT now()
);
CREATE TRIGGER map_group_user_power_modified BEFORE UPDATE ON map_group_user_power FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE INDEX ON map_group_user_power (group_id);
CREATE INDEX ON map_group_user_power (user_id);
CREATE INDEX ON map_group_user_power (power);
CREATE UNIQUE INDEX ON map_group_user_power (group_id, user_id, power);
INSERT INTO map_group_user_power (group_id, user_id, power) VALUES (1, 1, 1);

CREATE TABLE bulletins (
    id              serial          NOT NULL    PRIMARY KEY,
    group_id        integer         NOT NULL,
    setter_user_id  integer         NOT NULL,
    title           varchar(255)    DEFAULT '',
    content         text            DEFAULT '',
    created_at      timestamp       DEFAULT now(),
    updated_at      timestamp       DEFAULT now()
);
CREATE TRIGGER bulletins_modified BEFORE UPDATE ON bulletins FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE INDEX ON bulletins (group_id);
