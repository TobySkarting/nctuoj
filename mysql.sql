CREATE TABLE users (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `account`       varchar(32)     NOT NULL,
    `passwd`        varchar(32)     NOT NULL,
    `email`         varchar(255)    NOT NULL,
    `student_id`    varchar(16)     NOT NULL,
    `school_id`     int(11)         NOT NULL,
    `created_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;
INSERT INTO users (`account`, `passwd`, `email`, `student_id`, `school_id`) VALUES ('admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@gmail.com', '0000000', '0');

CREATE TABLE map_user_right (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `user_id`       int(11)         NOT NULL,
    `right`         int(11)         NOT NULL,
    `created_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX (`right`),
    INDEX (`user_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

INSERT INTO map_user_right (`user_id`, `right`) VALUES (1, 1);

CREATE TABLE user_right (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `description`   varchar(255),
    `created_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

INSERT INTO user_right (`description`) VALUES ('Users modify admin');

CREATE TABLE schools (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `name`          varchar(255)    NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

INSERT INTO schools (`name`) VALUES ("other");
INSERT INTO schools (`name`) VALUES ("NCTU 國立交通大學");

CREATE TABLE groups (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `name`          varchar(255)    NOT NULL,
    `description`   varchar(255)    NOT NULL,
    `created_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

INSERT INTO groups (`name`, `description`) VALUES ('Public', 'For Public');

CREATE TABLE map_group_user (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `group_id`      int(11)         NOT NULL,
    `user_id`       int(11)         NOT NULL,
    `created_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX (`group_id`),
    INDEX (`user_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

INSERT INTO map_group_user (`group_id`, `user_id`) VALUES (1, 1);

CREATE TABLE map_group_user_right (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `group_id`      int(11)         NOT NULL,
    `user_id`       int(11)         NOT NULL,
    `right`         int(11)         NOT NULL,
    PRIMARY KEY (`id`),
    INDEX (`group_id`),
    INDEX (`user_id`),
    INDEX (`right`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

INSERT INTO map_group_user_right (`group_id`, `user_id`, `right`) VALUES (1, 1, 1)

CREATE TABLE bulletins (
    `id`                int(11)         NOT NULL    AUTO_INCREMENT,
    `group_id`          int(11)         NOT NULL,
    `setter_user_id`    int(11)         NOT NULL,
    `title`             varchar(255)    ,
    `content`           text,
    `created_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX (`group_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

CREATE TABLE problems (
    `id`                int(11)         NOT NULL    AUTO_INCREMENT,
    `title`             varchar(255)    ,
    `description`       text            ,
    `input`             text            ,
    `output`            text            ,
    `sample_input`      text            ,
    `sample_output`     text            ,
    `hint`              text            ,
    `source`            text            ,
    `group_id`          int(11)         NOT NULL,
    `setter_user_id`    int(11)         NOT NULL,
    `visible`           int(11)         NOT NULL    DEFAULT 0,
    `interactive`       bool            NOT NULL    DEFAULT 0,
    `checker_id`        int(11)         ,
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`),
    INDEX(`visible`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;
# visible => 0 invisible for all, 1 visible in group, 2 visible in all

CREATE TABLE tags (
    `id`                int(11)         NOT 
)

CREATE TABLE checkers (
    `id`                int(11)         NOT NULL    AUTO_INCREMENT,
    `run_type_id`       int(11)         NOT NULL,
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

CREATE TABLE testdata (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `problem_id`    int(11)         NOT NULL,
    `order`         int(11)         NOT NULL,
    `time_limit`    int(11)         NOT NULL    DEFAULT 1000,
    `memory_limit`  int(11)         NOT NULL    DEFAULT 65536,
    `input_size`    int(11)         NOT NULL    DEFAULT 0,
    `output_size`   int(11)         NOT NULL    DEFAULT 0,
    `score`         int(11)                 ,
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`),
    INDEX (`problem_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

CREATE TABLE judge_problem_attachment (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `problem_id`    int(11)         NOT NULL,
    `run_type_id`   int(11)         NOT NULL,
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`),
    INDEX (`problem_id`),
    INDEX (`run_type_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

CREATE TABLE judge_testdata_attachment (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `testdata_id`   int(11)         NOT NULL,
    `run_type_id`   int(11)         NOT NULL,
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`),
    INDEX (`testdata_id`),
    INDEX (`run_type_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

CREATE TABLE submissions (
    `id`            int(11)     NOT NULL    AUTO_INCREMENT,
    `user_id`       int(11)     NOT NULL,
    `problem_id`    int(11)     NOT NULL,
    `run_type_id`   int(11)     NOT NULL,
    `time_usage`    int(6)              ,
    `memory_usage`  int(6)              ,
    `verdict`       int(6)      NOT NULL    DEFAULT 0,
    `score`         int(6)              ,
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX (`user_id`),
    INDEX (`problem_id`),
    INDEX (`run_type_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

CREATE TABLE wait_submissions (
    `id`            int(11)     NOT NULL    AUTO_INCREMENT,
    `submission_id` int(11)     NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

CREATE TABLE run_problem (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `problem_id`    int(11)         NOT NULL,
    `run_type_id`   int(11)         NOT NULL,
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`),
    INDEX (problem_id),
    INDEX (run_type_id)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;

CREATE TABLE run_type (
    `id`            int(11)         NOT NULL AUTO_INCREMENT,
    `description`   varchar(128)    NOT NULL DEFAULT "",
    `lang`          int(11)         NOT NULL,
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;


CREATE TABLE run_step (
    `id`            int(11)         NOT NULL    AUTO_INCREMENT,
    `run_type_id`   int(11)         NOT NULL,
    `step`          int(11)         NOT NULL,
    `command`       varchar(256)    NOT NULL    DEFAULT "",
    `primary`       bool            NOT NULL    DEFAULT false,
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`),
    INDEX(`run_type_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_unicode_ci;


