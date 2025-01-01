from fastapi import Depends

from .. import db, schema

from enum import StrEnum


async def create_user_table(db: db.Database = Depends(db.get_database)):
    """Create the users table"""
    query = (
        "CREATE TABLE IF NOT EXISTS users ("
        "    id TEXT NOT NULL,"
        "    email TEXT NOT NULL,"
        "    verified_email BOOLEAN NOT NULL,"
        "    name TEXT NOT NULL,"
        "    given_name TEXT NOT NULL,"
        "    family_name TEXT NOT NULL,"
        "    picture TEXT NOT NULL"
        ")"
    )
    create_indexes = (
        "CREATE INDEX IF NOT EXISTS idx_users_id ON users (id);"
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);"
    )
    return (
        await db.execute(query=query),
        await db.execute(query=create_indexes),
    )


async def create_user(
    user: schema.users.User,
    db: db.Database = Depends(db.get_database),
):
    """Create a New User"""
    query = (
        "INSERT INTO users ("
        " id, email, verified_email, name, given_name, family_name, picture) "
        "VALUES (:id, :email, :verified_email, :name, :given_name, :family_name, :picture)"
    )
    new_row_id = await db.execute(query=query, values=user.model_dump())
    return user


async def list_users(
    db: db.Database = Depends(db.get_database),
    page_options: schema.api.PageOptions = Depends(schema.api.PageOptions),
):
    """List all users"""
    query = "SELECT * FROM users"
    # TODO: Add pagination
    return await db.fetch_all(query=query)


async def get_user(user_id: str, db: db.Database = Depends(db.get_database)):
    """Get a user by ID"""
    query = "SELECT * FROM users WHERE id = :id"
    return await db.fetch_one(query=query, values={"id": user_id})
