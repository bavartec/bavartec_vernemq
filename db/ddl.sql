CREATE TABLE vmq_auth_acl
(
  username VARCHAR(64) NOT NULL,
  password BINARY(32) NOT NULL,
  salt CHAR(32) NOT NULL,
  CONSTRAINT vmq_auth_acl_primary_key PRIMARY KEY (username)
);
