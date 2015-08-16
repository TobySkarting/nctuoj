CREATE OR REPLACE FUNCTION update_modified_column() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified = now();
    RETURN NEW; 
END;
$$ language 'plpgsql';

CREATE TABLE users (
    id           int(11)         NOT NULL    AUTO_INCREMENT,
    account       varchar(32)     NOT NULL,
    passwd        varchar(32)     NOT NULL,
    email         varchar(255)    NOT NULL,
    student_id    varchar(16)     NOT NULL,
    school_id     int(11)         NOT NULL,
    created_at    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
};

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
