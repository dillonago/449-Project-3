#!/bin/sh

sqlite3 ./var/user.db< ./share/user.sql
sqlite3 ./var/game.db< ./share/game.sql
sqlite3 ./var/leaderboard.db< ./share/leaderboard.sql
python3 ./bin/copydata.py
