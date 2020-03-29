--------------------------------------------------------
-- Работа с пользователями
--------------------------------------------------------
-- Returns user id if login succeed, 
-- else rases error
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
    THEN RAISE EXCEPTION 'User is''t exists';
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
    INSERT INTO users.login(user_id, type_id, password) 
        VALUES(newid, p_type_id, p_password); 
    RETURN newid;
END;
$$ LANGUAGE plpgsql;


-- Returns True if autoprove completed successfully and adds approve record
-- Else returns False
DROP FUNCTION IF EXISTS users.prove_auto;
CREATE OR REPLACE FUNCTION users.prove_auto(
    IN p_user_id INTEGER
) RETURNS BOOLEAN AS $$
DECLARE 
    p_lastname VARCHAR(64);
    res BOOLEAN;
    ll users.login%rowtype;
BEGIN
    res := FALSE;
    --
    IF p_user_id NOT IN (SELECT DISTINCT up.id FROM users.profile up)
    THEN RAISE EXCEPTION 'User is''t exists';
    END IF;
    --
    p_lastname := (SELECT vpa.lastname 
    FROM users.v_profile_available vpa 
    WHERE id = p_user_id);
    --
    FOR ll IN 
        (SELECT *
        FROM users.login ul 
        WHERE ul.user_id = p_user_id)
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

--------------------------------------------------------
-- Работа с файлом
--------------------------------------------------------
