--------------------------------------------------------
-- Отладка
--------------------------------------------------------
DROP SCHEMA IF EXISTS 
    users,
    files,
    logs,
    automations CASCADE;


--------------------------------------------------------
-- Работа с пользователями
--------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS users;

DROP TABLE IF EXISTS users.type;

CREATE TABLE users.type(
    id SERIAL PRIMARY KEY,
    short_name VARCHAR(64) ,
    description TEXT
);

INSERT
    INTO
    users.type(
        id,
        short_name,
        description
    )
VALUES (
    1,
    'superuser',
    'User with administrator privileges, which can grants superusers.'
),
(
    2,
    'admin',
    'User with administrator privileges.'
),
(
    3,
    'user::tradeunion',
    'User which can login with tradeunion number and surname.'
),
(
    4,
    'user::student',
    'User which can login with student number and surname.'
);

CREATE TABLE IF NOT EXISTS users.profile(
    id SERIAL,
    firstname VARCHAR(64) ,
    lastname VARCHAR(64) ,
    middlename VARCHAR(64) ,
    birthday DATE ,
    email VARCHAR(256) ,
    vkid INTEGER,
    created TIMESTAMP DEFAULT NOW() ,
    PRIMARY KEY (id, created)
);

CREATE TABLE IF NOT EXISTS users.preregistred_profile(
    id SERIAL,
    firstname VARCHAR(64) ,
    lastname VARCHAR(64) ,
    middlename VARCHAR(64) ,
    birthday DATE ,
    email VARCHAR(256) ,
    type_id INTEGER ,
    PASSWORD VARCHAR(64) ,
    created TIMESTAMP DEFAULT NOW() ,
    expires TIMESTAMP ,
    PRIMARY KEY (id, created) ,
    FOREIGN KEY (type_id) REFERENCES users.type(id)
);

CREATE TABLE IF NOT EXISTS users.login(
    id SERIAL,
    profile_id INTEGER ,
    type_id INTEGER ,
    password VARCHAR(64) ,
    created TIMESTAMP DEFAULT NOW() ,
    PRIMARY KEY (id, created),
--    FOREIGN KEY (profile_id) REFERENCES users.profile(id) ,
    FOREIGN KEY (type_id) REFERENCES users.type(id)
);

CREATE TABLE IF NOT EXISTS users.approval(
    id SERIAL,
    login_id INTEGER ,
    binary_id INTEGER, --use lo_import and lo_export
    is_proved BOOLEAN ,
    created TIMESTAMP DEFAULT NOW() ,
    expires TIMESTAMP ,
    PRIMARY KEY (id, created)
--    FOREIGN KEY (login_id) REFERENCES users.login(id)
);

CREATE OR REPLACE
VIEW users.v_profile_available AS
SELECT
    up.id,
    up.firstname,
    up.lastname,
    up.middlename,
    up.birthday,
    up.email,
    up.vkid,
    ul.type_id,
    ul.PASSWORD,
    CASE WHEN ua.is_proved IS NULL THEN FALSE
    ELSE ua.is_proved END AS is_proved
FROM
    (
        SELECT
            *
        FROM
            users.profile up
        WHERE
            (
                up.id,
                up.created
            ) IN (
                SELECT
                    id,
                    MAX(created)
                FROM
                    users.profile up
                GROUP BY
                    id
            )
    ) up
LEFT JOIN (
        SELECT
            *
        FROM
            users.login ul
        WHERE
            (
                ul.id,
                ul.created
            ) IN (
                SELECT
                    id,
                    MAX(created)
                FROM
                    users.login up
                GROUP BY
                    id
            )
    ) ul ON
    up.id = ul.profile_id
LEFT JOIN (
        SELECT
            *
        FROM
            users.approval ua
        WHERE
            (
                ua.id,
                ua.created
            ) IN (
                SELECT
                    id,
                    MAX(created)
                FROM
                    users.approval ua
                GROUP BY
                    id
            )
            AND expires > NOW()
    ) ua ON
    ul.id = ua.login_id;


--------------------------------------------------------
-- Работа с файлами
--------------------------------------------------------
 CREATE SCHEMA IF NOT EXISTS files;

DROP TABLE IF EXISTS files.type;

CREATE TABLE files.type(
    id SERIAL PRIMARY KEY ,
    short_name VARCHAR(64) ,
    description TEXT
);

INSERT
    INTO
    files.type(
        id,
        short_name,
        description
    )
VALUES (
    1,
    'pdf',
    'PorTABLE Document Format by Adobe'
);

CREATE TABLE IF NOT EXISTS files.file(
    id SERIAL ,
    pin INTEGER ,
    profile_id INTEGER ,
    type_id INTEGER ,
    hash VARCHAR(32) ,
    SIZE INTEGER ,
    page_count INTEGER ,
    binary_id INTEGER, --use lo_import and lo_export
    created TIMESTAMP DEFAULT NOW() ,
    PRIMARY KEY (id, created),
--    FOREIGN KEY (profile_id) REFERENCES users.profile(id) ,
    FOREIGN KEY (type_id) REFERENCES files.type(id)
);

CREATE TABLE IF NOT EXISTS files.option(
    id SERIAL,
    file_id INTEGER ,
    pages VARCHAR(64) ,
    count_per_list INTEGER ,
    twosided BOOLEAN ,
    created TIMESTAMP DEFAULT NOW() ,
    PRIMARY KEY (id, created)
--    FOREIGN KEY (file_id) REFERENCES files.file(id)
);


--------------------------------------------------------
--Работа с логом
--------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS logs;

DROP TABLE IF EXISTS logs.type;

CREATE TABLE logs.type(
    id SERIAL PRIMARY KEY ,
    short_name VARCHAR(64) ,
    description TEXT
);

INSERT
    INTO
    files.type(
        id,
        short_name,
        description
    )
VALUES (
    100,
    'UserAction',
    'Miscellaneous action with users'
),
(
    101,
    'UserAddProfile',
    'User add profile'
),
(
    102,
    'UserAddLogin',
    'User add login'
),
(
    103,
    'UserDelete',
    'User wipe'
),
(
    104,
    'UserConfirm',
    'User login confirmation by admin'
),
(
    105,
    'UserAutoconfirm',
    'User login confirmation by preregistred users'
),
(
    106,
    'UserEdit',
    'User parameters edit by admin'
),
(
    200,
    'FileAction',
    'Miscellaneous action with files'
),
(
    201,
    'FileAdd',
    'File uploaded by user'
),
(
    202,
    'FileDelete',
    'File deleted from server'
),
(
    203,
    'FileOptionsAdd',
    'File options added'
),
(
    300,
    'VkbotAction',
    'Miscellaneous action with VK bot'
),
(
    301,
    'VkbotLogin',
    'VK bot signed in'
),
(
    302,
    'VkbotButtonClick',
    'VK bot used'
),
(
    400,
    'WebappAction',
    'Miscellaneous action with Web app'
),
(
    401,
    'WebappLogin',
    'Web app signed in'
),
(
    402,
    'WebappButtonClick',
    'Web app used'
),
(
    500,
    'TerminalappAction',
    'Miscellaneous action with terminal app'
),
(
    501,
    'TerminalappLogin',
    'Terminal app signed in'
),
(
    502,
    'TerminalappButtonClick',
    'Terminal app used'
),
(
    503,
    'TerminalappPrint',
    'Terminal app sent document to printer'
);

CREATE TABLE IF NOT EXISTS logs.record(
    id SERIAL ,
    created TIMESTAMP DEFAULT NOW() ,
    issuer_id INTEGER ,
    profile_id INTEGER ,
    file_id INTEGER ,
    type_id INTEGER ,
    message TEXT ,
    -- FOREIGN KEY (issuer_id) REFERENCES pg_catalog.pg_user(usesysid),
    PRIMARY KEY (id, created) ,
--    FOREIGN KEY (profile_id) REFERENCES users.profile(id) ,
--    FOREIGN KEY (file_id) REFERENCES files.file(id) ,
    FOREIGN KEY (type_id) REFERENCES logs.type(id)
);
