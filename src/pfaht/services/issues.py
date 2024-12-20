from fastapi import Depends

from .. import db, schema

from enum import StrEnum


async def create_issue_table(db: db.Database = Depends(db.get_database)):
    """Create the issues table"""
    query = (
        "CREATE TABLE IF NOT EXISTS issues ("
        "    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "    issue_title TEXT NOT NULL,"
        "    issue_body TEXT NOT NULL,"
        "    issue_status TEXT NOT NULL"
        ")"
    )
    return await db.execute(query=query)


async def create_issue(
    new_issue: schema.issues.NewIssue,
    db: db.Database = Depends(db.get_database),
):
    """Create a New Issue

    Parameters:
    -----------
        new_issue (schema.issues.NewIssue): The new issue to create

    Returns:
    --------
        schema.devices.Device: The newly created device

    """
    query = (
        "INSERT INTO issues (issue_title, issue_body, issue_status) "
        "VALUES (:issue_title, :issue_body, :issue_status)"
    )
    new_row_id = await db.execute(query=query, values=new_issue.model_dump())
    return schema.issues.IssueServiceResponse(
        await get_issue(new_row_id, db),
        db=db,
    )


async def delete_issue(issue_id: int, db: db.Database = Depends(db.get_database)):
    """Delete a device by ID

    Parameters:
    -----------
        issue_id (int): The ID of the device to delete
        db (db.Database): The database connection
    """
    query = "DELETE FROM devices WHERE issue_id = :issue_id"
    return await db.execute(query=query, values={"issue_id": issue_id})


async def list_issues(
    db: db.Database = Depends(db.get_database),
    page_options: schema.api.PageOptions = Depends(schema.api.PageOptions),
) -> schema.issues.IssueListServiceResponse:
    """List all issues

    Returns:
    --------
        list[schema.issues.Issues]: A list of all issues in the database
    """
    query = "SELECT * FROM issues LIMIT :per_page OFFSET :offset"
    issues = await db.fetch_all(
        query=query,
        values={"per_page": page_options.per_page, "offset": page_options.offset},
    )
    return schema.issues.IssueListServiceResponse(
        data=[schema.issues.Issue.model_validate(dict(issue)) for issue in issues],
        db=db,
        page_options=page_options,
    )


async def get_issue(
    issue_id: int,
    db: db.Database = Depends(db.get_database),
) -> schema.issues.IssueServiceResponse:
    """Get a device by ID

    Parameters:
    -----------
        issue_id (int): The ID of the issue to retrieve

    Returns:
    --------
        schema.issues.Issue: The issue with the specified ID
    """
    query = "SELECT * FROM issues WHERE issue_id = :issue_id"
    issue = await db.fetch_one(query=query, values={"issue_id": issue_id})

    if issue is None:
        schema.devices.MissingDeviceResponse(
            response=None, message=f"Device {issue_id} not found"
        )

    return schema.issues.IssueServiceResponse(
        data=schema.issues.Issue.model_validate(dict(issue)),
        db=db,
    )


async def update_issue(
    issue_id: int,
    updated_issue: schema.issues.NewIssue,
    db: db.Database = Depends(db.get_database),
) -> schema.issues.IssueServiceResponse:
    """
    Update a device by ID

    Parameters:
    -----------
        issue_id (int): The ID of the device to update
        updated_issue (schema.issues.NewIssue): The updated issue information
            to apply to the issue with the specified ID
        db (db.Database): The database connection
    """
    query = (
        "UPDATE issues SET "
        "issue_title = :issue_title, "
        "issue_body = :issue_body, "
        "issue_status = :issue_status "
        "WHERE issue_id = :issue_id"
    )
    await db.execute(
        query=query, values={**update_issue.model_dump(), "issue_id": issue_id}
    )

    device = await get_issue(issue_id, db)
    return device


async def list_device_types() -> list[str]:
    """List all valid device types

    The valid device types are going to be ones that we have svg\'s for in the
    templates directory.

    Returns:
    --------
        list[str]: A list of all valid device types
    """
    from ..web.html import template_path

    # for each file in the svgrepo directory, get the name of the file without the extension
    return [f.stem for f in template_path.glob("svgrepo/*.svg")]
