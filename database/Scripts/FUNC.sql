--------------------------------------------------------
-- Работа с пользователями
--------------------------------------------------------
-- Returns user id if login succeed, 
-- else returns -1
DROP FUNCTION IF EXISTS users.login;
CREATE OR REPLACE FUNCTION users.login(
    IN p_type_id INTEGER,
    IN p_login VARCHAR(64),
    IN p_password VARCHAR(64)
) RETURNS INTEGER AS $$ 
DECLARE loginid INTEGER;
BEGIN
    --
    IF     (p_type_id IS NULL) 
        OR (p_login IS NULL) 
        OR (p_password IS NULL) 
    THEN RAISE EXCEPTION 'Arg must be notnull'; 
    END IF;
    --
    loginid := (SELECT id
    FROM users.v_profile_available upa
    WHERE upa.type_id = p_type_id 
          AND TRIM(UPPER(upa.lastname)) = TRIM(UPPER(p_login))
          AND upa.password = p_password); 
    -- 
    IF loginid IS NULL 
    THEN RETURN -1;
    ELSE RETURN loginid;
    END IF;
    --
END;
$$ LANGUAGE plpgsql;


-- Returns new user id if no such user already exists, 
-- else raises error
DROP FUNCTION IF EXISTS users.register;
CREATE OR REPLACE FUNCTION users.register(
    IN p_type_id INTEGER,
    IN p_login VARCHAR(64),
    IN p_password VARCHAR(64)
) RETURNS INTEGER AS $$
DECLARE newid INTEGER;
BEGIN
    --
    IF     (p_type_id IS NULL) 
        OR (p_login IS NULL) 
        OR (p_password IS NULL) 
    THEN RAISE EXCEPTION 'Arg must be notnull'; 
    END IF;
    --
    IF (SELECT COUNT(*) > 0
        FROM users.login l
        WHERE l.type_id = p_type_id AND l.password = p_password)
    THEN RAISE EXCEPTION 'User already registred';
    END IF;
    --
    newid := nextval('users.profile_id_seq'::regclass);
    INSERT INTO users.profile(id, lastname) 
        VALUES(newid, p_login);
    INSERT INTO users.login(profile_id, type_id, password) 
        VALUES(newid, p_type_id, p_password); 
    RETURN newid;
END;
$$ LANGUAGE plpgsql;


-- Returns True if autoprove completed successfully and adds approve record
-- Else returns False
DROP FUNCTION IF EXISTS users.prove_auto;
CREATE OR REPLACE FUNCTION users.prove_auto(
    IN p_profile_id INTEGER
) RETURNS BOOLEAN AS $$
DECLARE 
    p_lastname VARCHAR(64);
    res BOOLEAN;
    ll users.login%rowtype;
BEGIN
    res := FALSE;
    --
    IF p_profile_id NOT IN (SELECT DISTINCT up.id FROM users.profile up)
    THEN RAISE EXCEPTION 'User is''t exists';
    END IF;
    --
    p_lastname := (SELECT vpa.lastname 
    FROM users.v_profile_available vpa 
    WHERE id = p_profile_id);
    --
    FOR ll IN 
        (SELECT *
        FROM users.login ul 
        WHERE ul.profile_id = p_profile_id)
    LOOP 
        IF (SELECT COUNT(DISTINCT pp.id) = 1 FROM users.preregistred_profile pp
            WHERE (pp.type_id, pp.password, TRIM(UPPER(pp.lastname))) = (ll.type_id, ll.password, TRIM(UPPER(p_lastname))))
        THEN 
            res := TRUE;
            INSERT INTO users.approval (login_id, is_proved, expires) VALUES (
                ll.id,
                TRUE,
                (SELECT MAX(pp2.expires)
                    FROM users.preregistred_profile pp2
                    WHERE (pp2.type_id, pp2.password, pp2.lastname) = (ll.type_id, ll.password, p_lastname))
            );
        END IF;
    END LOOP;
    --
    RETURN res;
END;
$$ LANGUAGE plpgsql;


-- Returns status_code=202 if user allowed to print and it's profile_id
-- Else returns status_code=204 if user not allowed to print and it's profile_id
-- If user does't exists, creates new, returns status_code=201 and it's profile_id. 
DROP FUNCTION IF EXISTS users.signin_routine;
CREATE OR REPLACE FUNCTION users.signin_routine(
    IN p_type_id INTEGER,
    IN p_login VARCHAR(64),
    IN p_password VARCHAR(64)
) RETURNS TABLE(status_code INTEGER, status_message TEXT, profile_id INTEGER) AS $$ 
DECLARE
    p_profile_id INTEGER;
BEGIN 
    p_profile_id = users.login(p_type_id, p_login, p_password);
    IF p_profile_id = -1 THEN p_profile_id = users.register(p_type_id, p_login, p_password); END IF;
        -- Пользователь существует, проверяем на возможность печати
    IF (SELECT TRUE IN (vpa.is_proved) 
        FROM users.v_profile_available vpa 
        WHERE vpa.id = p_profile_id)
    THEN RETURN QUERY SELECT 202, 'Пользователь успешно вошел в систему', p_profile_id;
    ELSE 
        IF (users.prove_auto (p_profile_id))
        THEN RETURN QUERY SELECT 202, 'Пользователь успешно вошел в систему', p_profile_id;
        ELSE RETURN QUERY SELECT 201, 'Пользователь успешно вошел в систему, но не имеет прав для печати', p_profile_id;
        END IF;
    END IF;
END; $$ LANGUAGE plpgsql;


-- Returns 200 and tradeunion number if exists
-- Else returns 404 if user not exits or 405 if exists more than one
DROP FUNCTION IF EXISTS users.find_tradeunion_number;
CREATE OR REPLACE FUNCTION users.find_tradeunion_number(
    IN p_firstname VARCHAR(64),
    IN p_lastname VARCHAR(64),
    IN p_birthdate DATE
) RETURNS TABLE(status_code INTEGER, status_message TEXT, tradeunion_number VARCHAR(64)) AS $$ 
DECLARE 
    cnt INTEGER;
BEGIN 
    cnt := (SELECT COUNT(DISTINCT password) 
        FROM users.preregistred_profile
        WHERE   firstname=p_firstname
            AND lastname=p_lastname
            AND birthday=p_birthdate
            AND type_id=3);
    CASE cnt
    WHEN 0 THEN RETURN QUERY (SELECT 404, 'Номер не найден', NULL::VARCHAR(64));
    WHEN 1 THEN RETURN QUERY
        (SELECT 200, 'Поиск завершился успешно', password 
        FROM users.preregistred_profile
        WHERE   firstname=p_firstname
            AND lastname=p_lastname
            AND birthday=p_birthdate
            AND type_id=3);
    ELSE RETURN QUERY SELECT (405, 'По запросу найдено более одного человека', NULL::VARCHAR(64));
    END CASE;
END; $$ LANGUAGE plpgsql;

-- Returns 200 and student number if exists
-- Else returns 404 if user not exits or 405 if exists more than one
DROP FUNCTION IF EXISTS users.find_student_number;
CREATE OR REPLACE FUNCTION users.find_student_number(
    IN p_firstname VARCHAR(64),
    IN p_lastname VARCHAR(64),
    IN p_birthdate DATE
) RETURNS TABLE(status_code INTEGER, status_message TEXT, student_number VARCHAR(64)) AS $$
DECLARE 
    cnt INTEGER;
BEGIN 
    cnt := (SELECT COUNT(DISTINCT password) 
        FROM users.preregistred_profile
        WHERE   firstname=p_firstname
            AND lastname=p_lastname
            AND birthday=p_birthdate
            AND type_id=4);
    CASE cnt
    WHEN 0 THEN RETURN QUERY (SELECT 404, 'Номер не найден', NULL::VARCHAR(64));
    WHEN 1 THEN RETURN QUERY
        (SELECT 200, 'Поиск завершился успешно', password 
        FROM users.preregistred_profile
        WHERE   firstname=p_firstname
            AND lastname=p_lastname
            AND birthday=p_birthdate
            AND type_id=4);
    ELSE RETURN QUERY (SELECT 405, 'По запросу найдено более одного человека', NULL::VARCHAR(64));
    END CASE;
END; $$ LANGUAGE plpgsql;

--------------------------------------------------------
-- Работа с файлом
--------------------------------------------------------
