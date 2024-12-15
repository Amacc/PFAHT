import sqlite3
from functools import partial
from typing import AsyncGenerator

from databases import Database

from . import dist_name


def get_connection(file: str) -> sqlite3.Connection:
    """Connect to a SQLite database file and return the connection."""
    return sqlite3.connect(file)

pfaht_db_file = f"{dist_name}.db"
get_self_db = partial(get_connection, f"./{pfaht_db_file}")

async def get_database() -> AsyncGenerator[Database, None]:
    """Create a Database instance, connect to it, and yield it.
    
    This function is an async generator, so it can be used in a context manager,
    or in the fastapi Depends function.
    """
    db = Database(f"sqlite+aiosqlite:///{pfaht_db_file}")
    await db.connect()
    yield db
    await db.disconnect()
