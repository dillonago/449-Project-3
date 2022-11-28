#!/bin/sh

sqlite3 ./var/user.db< ./share/user.sql
sqlite3 ./var/game.db< ./share/game.sql
python3 ./bin/copydata.py
