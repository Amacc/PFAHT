from fastapi import Depends

from .. import db, schema

from enum import StrEnum


async def create_user_table(db: db.Database = Depends(db.get_database)):
    """Create the users table"""
    create_user_table = (
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
    create_unique_index_user_id = (
        "CREATE UNIQUE INDEX IF NOT EXISTS unique_idx_users_id ON users (id);"
    )
    create_index_user_email = (
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);"
    )
    create_group_table = (
        "CREATE TABLE IF NOT EXISTS groups ("
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "    name TEXT NOT NULL"
        ")"
    )
    create_group_table_name_index = (
        "CREATE UNIQUE INDEX IF NOT EXISTS unique_idx_groups_name ON groups (name);"
    )
    create_user_group_table = (
        "CREATE TABLE IF NOT EXISTS user_groups ("
        "    user_id TEXT NOT NULL,"
        "    group_id INTEGER NOT NULL,"
        "    PRIMARY KEY (user_id, group_id),"
        "    FOREIGN KEY (user_id) REFERENCES users (id),"
        "    FOREIGN KEY (group_id) REFERENCES groups (id)"
        ")"
    )

    return [
        await db.execute(query=query)
        for query in (
            create_user_table,
            create_unique_index_user_id,
            create_index_user_email,
            create_group_table,
            create_group_table_name_index,
            create_user_group_table,
        )
    ]


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
    query = "SELECT * FROM users LIMIT :per_page OFFSET :offset"
    users = await db.fetch_all(
        query=query,
        values={"per_page": page_options.per_page, "offset": page_options.offset},
    )
    return [schema.users.User.model_validate(dict(user)) for user in users]


async def get_user(user_id: str, db: db.Database = Depends(db.get_database)):
    """Get a user by ID"""
    query = "SELECT * FROM users WHERE id = :id"
    return await db.fetch_one(query=query, values={"id": user_id})


async def delete_user(user_id: str, db: db.Database = Depends(db.get_database)):
    """Delete a user by ID"""
    query = "DELETE FROM users WHERE id = :id"
    return await db.execute(query=query, values={"id": user_id})


async def add_user_to_group(
    user_id: str,
    group_id: str,
    db: db.Database = Depends(db.get_database),
):
    """Add a user to a group"""
    query = "INSERT INTO user_groups (user_id, group_id) VALUES (:user_id, :group_id)"
    return await db.execute(
        query=query, values={"user_id": user_id, "group_id": group_id}
    )


async def list_groups(
    db: db.Database = Depends(db.get_database),
    page_options: schema.api.PageOptions = Depends(schema.api.PageOptions),
) -> schema.users.GroupListServiceResponse:
    """List all groups"""
    query = "SELECT * FROM groups LIMIT :per_page OFFSET :offset"
    groups = await db.fetch_all(
        query=query,
        values={"per_page": page_options.per_page, "offset": page_options.offset},
    )
    groups = [schema.users.Group.model_validate(dict(group)) for group in groups]
    return schema.users.GroupListServiceResponse(
        data=groups,
        db=db,
    )


async def create_group(
    group: schema.users.NewGroup,
    db: db.Database = Depends(db.get_database),
) -> schema.users.GroupServiceResponse:
    """Create a New Group"""
    query = "INSERT INTO groups (name) VALUES (:name)"
    new_row_id = await db.execute(query=query, values=group.model_dump())

    return await get_group(new_row_id, db)


async def get_group(
    group_id: str, db: db.Database = Depends(db.get_database)
) -> schema.users.GroupServiceResponse:
    query = "SELECT * FROM groups WHERE id = :id"
    group = await db.fetch_one(query=query, values={"id": group_id})
    return schema.users.GroupServiceResponse(
        data=schema.users.Group.model_validate(dict(group)),
        db=db,
    )


async def assign_group_to_user(
    user_id: str,
    group_id: str,
    db: db.Database = Depends(db.get_database),
):
    """Assign a group to a user"""
    query = "INSERT INTO user_groups (user_id, group_id) VALUES (:user_id, :group_id)"
    return await db.execute(
        query=query, values={"user_id": user_id, "group_id": group_id}
    )
