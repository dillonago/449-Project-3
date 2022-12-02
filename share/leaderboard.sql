PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS Leaderboard;
CREATE TABLE Leaderboard(game_id VARCHAR PRIMARY KEY, user VARCHAR, game_status VARCHAR, score INTEGER);

INSERT INTO Leaderboard(game_id, user, game_status, score) VALUES ("12345", "newuser", "Won in 1 guess", 6);
INSERT INTO Leaderboard(game_id, user, game_status, score) VALUES ("11223", "newuser", "Won in 3 guesses", 4);
INSERT INTO Leaderboard(game_id, user, game_status, score) VALUES ("54321", "newuser", "Won in 5 guesses", 2);

COMMIT;