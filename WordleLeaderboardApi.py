
from cmath import e
import collections
import dataclasses
import textwrap
import sqlite3
import databases
import toml
import random
import uuid

from quart import Quart, g, request, abort
# from quart_auth import basic_auth_required

from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)

app.config.from_file(f"./etc/{__name__}.toml", toml.load)


@dataclasses.dataclass
class game:
    game_id: str
    game_status: str
    score: int


async def _get_db():
    db = getattr(g, "_sqlite_db", None)
    if db is None:
        db = g._sqlite_db = databases.Database(app.config["DATABASES"]["URL"])
        await db.connect()
    return db

@app.teardown_appcontext
async def close_connection(exception):
    db = getattr(g, "_sqlite_db", None)
    if db is not None:
        await db.disconnect()

@app.route("/")
def index():
    return textwrap.dedent(
        """
        <h1>Welcome to the Wordle</h1>

        """
    )


@app.errorhandler(RequestSchemaValidationError)
def bad_request(e):
    return {"error": str(e.validation_error)}, 400


@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409


@app.errorhandler(401)
def not_found(e):
    return {"error": "Unauthorized"}, 401


# Start of Game API

@app.errorhandler(404)
def not_found(e):
    return {"error": str(e)}, 404

# New Game API
@app.route("/leaderboard", methods=["POST"])
@validate_request(game)
async def postgame(data):
    db = await _get_db()
    auth=request.authorization
    game = dataclasses.asdict(data)
    
    try:
        leaderboard_game = await db.execute("INSERT INTO Leaderboard(game_id, game_status, score) VALUES (:game_id, :game_status, :score)", values=game)
    except sqlite3.IntegrityError as e:
        abort(409, e)

    return game, 200


@app.errorhandler(417)
def not_found(e):
    return {"error": str(e)}, 417

