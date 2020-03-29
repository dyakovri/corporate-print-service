-- Returns user id if login succeed, else returns NULL
DROP FUNCTION IF EXISTS automations.login;
CREATE OR REPLACE FUNCTION automations.login(
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


-- Returns user id if no such user already exists, else returns error
DROP FUNCTION IF EXISTS automations.register;
CREATE OR REPLACE FUNCTION automations.register(
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
