-- $ sqlite3 ./var/user.db < ./share/user.sql


PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS User;
CREATE TABLE User(username VARCHAR PRIMARY KEY, password VARCHAR,UNIQUE(username, password));

INSERT INTO User(username, password) VALUES ("Alejandro", "pass123");
INSERT INTO User(username, password) VALUES ("Shreya", "pass456");
INSERT INTO User(username, password) VALUES ("Manan", "pass789");
INSERT INTO User(username, password) VALUES ("Dillon", "pass101");

COMMIT;

