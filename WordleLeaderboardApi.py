from cmath import e
import dataclasses
import textwrap
import sqlite3
import databases
import toml
import redis
import json
from quart import Quart, g, request, abort, jsonify
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request, tag

app = Quart(__name__)
QuartSchema(app, tags=[
    {"name": "Root", "description": "Root path."},
    {"name": "Leaderboard", "description": "APIs for leaderboard."}])

app.config.from_file(f"./etc/{__name__}.toml", toml.load)

leaderboard = redis.Redis()

@dataclasses.dataclass
class game:
    game_id: str
    user: str
    game_status: str
    score: int

# route endpoint.
@app.route("/")
@tag(["Root"])
def index():
    """ Returns HTML content. """
    return textwrap.dedent(
        """
        <h1>Welcome to the Wordle</h1>

        """
    )

# status codes
@app.errorhandler(RequestSchemaValidationError)
def bad_request(e):
    return {"error": str(e.validation_error)}, 400

@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409

@app.errorhandler(401)
def not_found(e):
    return {"error": "Unauthorized"}, 401

@app.errorhandler(404)
def not_found(e):
    return {"error": str(e)}, 404

# New Game API
@app.route("/leaderboard", methods=["POST"])
@tag(["Leaderboard"])
@validate_request(game)
async def postgame(data):
    """ Save game result into database. """
    auth=request.authorization
    game = dataclasses.asdict(data)
    game_id = game["game_id"]
    #insert user and game status into hash at game_id key
    leaderboard.hset(game_id, "user", game["user"])
    leaderboard.hset(game_id, "game_status", game["game_status"])

    #insert score into sorted set at game_id key
    leaderboard.zadd("scores", {game_id: game["score"]})

    app.logger.info(leaderboard.hgetall(game_id))
    app.logger.info(leaderboard.zscore("scores", game_id))
    return game, 200


# status code
@app.errorhandler(417)
def not_found(e):
    return {"error": str(e)}, 417