from flask import current_app
from hwalloc.db import get_db

def get_device_list():
    db = get_db()
    cursor = db.execute(
        'SELECT'
        '    uuid,'
        '    allocation_count'
        ' FROM'
        '     device'
    )
    return [{"uuid": row[0], "allocation_count": row[1]} for row in cursor.fetchall()]

def create_device(uuid, db = None):
    commit_here = True

    if db is None:
        db = get_db()
        commit_here = False
    
    db.execute(
        'INSERT OR IGNORE INTO device (uuid, allocation_count)'
        ' VALUES (?, 0)',
        (uuid,)
    )

    if commit_here: db.commit()

def get_device(uuid):
    error = None
    db = get_db()
    cursor = db.execute(
        'SELECT uuid, allocation_count FROM device WHERE uuid = ?',
        (uuid,)
    )
    row = cursor.fetchone()

    device = {"uuid": row['uuid'], "allocation_count": row['allocation_count']}

    if device is None:
        error = f"No device with uuid { uuid } was found."
    return device, error

def get_next_device():
    """Get the next allocatable device or return none."""
    device = None
    error = None
    db = get_db()
    cursor = db.execute(
        'SELECT'
        '  uuid,'
        '  allocation_count'
        ' FROM'
        '  device'
        ' WHERE'
        '  allocation_count = ('
        '    SELECT min(allocation_count) FROM device'
        '  )'
    )
    row = cursor.fetchone()
    if row is None:
        error = f"No next device found. Have devices been added to the database?"
    else:
        device = {"uuid": row['uuid'], "allocation_count": row['allocation_count']}
    return device, error

def allocate_device(uuid = None):
    """Allocate a device."""
    device = None
    error = None
    oversubscribe = current_app.config['DEVICE_OVERSUBSCRIBE']
    if uuid is None:
        device, error = get_next_device()
    else:
        device, error = get_device(uuid)

    if device is not None:
        if device['allocation_count'] > 0 and not oversubscribe:
            error = f"Request for uuid:{device['uuid']} results in oversubscription."
        else:
            db = get_db()
            db.execute(
                'UPDATE device'
                ' SET allocation_count = allocation_count + 1'
                ' WHERE uuid = ?',
                (device['uuid'],)
            )
            db.commit()
            device, error = get_device(device['uuid'])

    return device, error

def release_device(uuid):
    """Release a device allocation"""
    device, error = get_device(uuid)
    if device['allocation_count'] < 1:
        error = f"The device with uuid {uuid} appears to already be unallocated"
    else:
        db = get_db()
        db.execute(
            'UPDATE device'
            ' SET allocation_count = allocation_count - 1'
            ' WHERE uuid = ?',
            (device['uuid'],)
        )
        db.commit()
        device, error = get_device(device['uuid'])
    
    return device, error