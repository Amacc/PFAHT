
from fastapi import Depends

from .. import db, schema


async def create_device_table(
    db: db.Database = Depends(db.get_database)
):
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

async def list_devices(
    db: db.Database = Depends(db.get_database)
) -> list[schema.devices.Device]:
    """List all devices
    
    Returns:
    --------
        list[schema.devices.Device]: A list of all devices in the database
    """
    query = "SELECT * FROM devices"
    devices = await db.fetch_all(query=query)
    return [schema.devices.Device.model_validate(dict(device)) for device in devices]


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
    new_row_id = await db.execute(query=query, values=new_device.dict())
    return await get_device(new_row_id, db)

async def get_device(
    device_id: int,
    db: db.Database = Depends(db.get_database)
):
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
        schema.devices.MissingDeviceResponse(response=None, message=f"Device {device_id} not found")

    return schema.devices.Device.model_validate(dict(device))
