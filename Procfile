game: hypercorn WordleGameApi --reload --debug --bind WordleGameApi.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
user: hypercorn WordleUserApi --reload --debug --bind WordleUserApi.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
leaderboard: hypercorn WordleLeaderboardApi --reload --debug --bind WordleLeaderboardApi.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
