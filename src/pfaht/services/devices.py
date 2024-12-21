from fastapi import Depends

from .. import db, schema


async def create_device_table(db: db.Database = Depends(db.get_database)):
    """Create the devices table"""
    query = (
        "CREATE TABLE IF NOT EXISTS devices ("
        "    device_id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "    device_name TEXT NOT NULL,"
        "    device_type TEXT NOT NULL,"
        "    device_location TEXT NOT NULL"
        ")"
    )
    return await db.execute(query=query)


async def create_device(
    new_device: schema.devices.NewDevice,
    db: db.Database = Depends(db.get_database),
):
    """Create a new device

    Parameters:
    -----------
        new_device (schema.devices.NewDevice): The new device to create

    Returns:
    --------
        schema.devices.Device: The newly created device

    """
    query = (
        "INSERT INTO devices (device_name, device_type, device_location) "
        "VALUES (:device_name, :device_type, :device_location)"
    )
    new_row_id = await db.execute(query=query, values=new_device.model_dump())
    return await get_device(new_row_id, db)


async def delete_device(device_id: int, db: db.Database = Depends(db.get_database)):
    """Delete a device by ID

    Parameters:
    -----------
        device_id (int): The ID of the device to delete
        db (db.Database): The database connection
    """
    query = "DELETE FROM devices WHERE device_id = :device_id"
    await db.execute(query=query, values={"device_id": device_id})


async def list_devices(
    db: db.Database = Depends(db.get_database),
    page_options: schema.api.PageOptions = Depends(schema.api.PageOptions),
) -> list[schema.devices.Device]:
    """List all devices

    Returns:
    --------
        list[schema.devices.Device]: A list of all devices in the database
    """
    query = "SELECT * FROM devices LIMIT :per_page OFFSET :offset"
    devices = await db.fetch_all(
        query=query,
        values={"per_page": page_options.per_page, "offset": page_options.offset},
    )
    return [schema.devices.Device.model_validate(dict(device)) for device in devices]


async def get_device(device_id: int, db: db.Database = Depends(db.get_database)):
    """Get a device by ID

    Parameters:
    -----------
        device_id (int): The ID of the device to retrieve

    Returns:
    --------
        schema.devices.Device: The device with the specified ID
    """
    query = "SELECT * FROM devices WHERE device_id = :device_id"
    device = await db.fetch_one(query=query, values={"device_id": device_id})

    if device is None:
        schema.devices.MissingDeviceResponse(
            response=None, message=f"Device {device_id} not found"
        )

    return schema.devices.Device.model_validate(dict(device))


async def update_device(
    device_id: int,
    updated_device: schema.devices.NewDevice,
    db: db.Database = Depends(db.get_database),
) -> schema.devices.Device:
    """
    Update a device by ID

    Parameters:
    -----------
        device_id (int): The ID of the device to update
        updated_device (schema.devices.NewDevice): The updated device information
            to apply to the device with the specified ID
        db (db.Database): The database connection
    """
    query = (
        "UPDATE devices "
        "SET device_name = :device_name, device_type = :device_type, device_location = :device_location "
        "WHERE device_id = :device_id"
    )
    await db.execute(
        query=query, values={**updated_device.model_dump(), "device_id": device_id}
    )

    device = await get_device(device_id, db)
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
