INSERT INTO vmq_auth_acl
    (username, password, salt)
VALUES
    ('test-user1', UNHEX(SHA2(CONCAT('test-pass1', 'salt1'), 256)), 'salt1'),
    ('test-user2', UNHEX(SHA2(CONCAT('test-pass2', 'salt2'), 256)), 'salt2'),
    ('test-user3', UNHEX(SHA2(CONCAT('test-pass3', 'salt3'), 256)), 'salt3');
