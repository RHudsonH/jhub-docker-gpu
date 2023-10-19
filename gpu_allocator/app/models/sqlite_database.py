import sqlite3
from app.config import Config
from .database_interface import DatabaseInterface
    
class SQLiteDatabase(DatabaseInterface):
    def __init__(self, oversubscribe_limit):
        super().__init__(oversubscribe_limit)
        self.conn = sqlite3.connect('devices.db', check_same_thread=False)
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS devices (uuid TEXT PRIMARY KEY, allocation_count INTEGER)"
            )

    def update_devices(self, devices):
        with self.conn:
            for device in devices:
                self.conn.execute(
                    "INSERT OR IGNORE INTO devices (uuid, allocation_count) VALUES (?, 0)",
                    (device,)
                )

    def list_devices(self):
        cursor = self.conn.execute("SELECT uuid, allocation_count FROM devices")
        return [{"uuid": row[0], "allocation_count": row[1]} for row in cursor.fetchall()]
    
    def get_device(self, uuid):
        cursor = self.conn.execute(
            "SELECT uuid, allocation_count FROM devices WHERE uuid = ?",
            (uuid,)
        )
        row = cursor.fetchone()
        return {"uuid": row[0], "allocation_count": row[1]} if row else None
    
    def allocate_device(self, uuid = None):
        with self.conn:
            if uuid: # If a specific UUID is requested try to allocate it.
                cursor = self.conn.execute(
                    "SELECT allocation_count FROM devices WHERE uuid = ?",
                    (uuid,)
                )
                row = cursor.fetchone()
                if row and row[0] < self.oversubscribe_limit:
                    self.conn.execute(
                        "UPDATE devices SET allocation_count = allocation_count + 1 WHERE uuid =?",
                        (uuid,)
                    )
                    return {"uuid": uuid, "allocation_count": row[0] +1}
            else: #If no UUID is provided, find the next available device.
                cursor = self.conn.execute(
                    "SELECT uuid, allocation_count FROM devices WHERE allocation_count < ? ORDER BY allocation_count ASC LIMIT 1",
                    (self.oversubscribe_limit,)
                )
                row = cursor.fetchone()
                if row:
                    uuid = row[0]
                    self.conn.execute(
                        "UPDATE devices SET allocation_count = allocation_count + 1 WHERE uuid = ?",
                        (uuid,)
                    )
                    return {"uuid": uuid, "allocation_count": row[1] + 1}
        return None
    
    def release_device(self, uuid):
        with self.conn:
            cursor = self.conn.execute(
                "SELECT allocation_count FROM devices WHERE uuid = ?",
                (uuid,)
            )
            row = cursor.fetchone()
            if row and row[0] > 0:
                self.conn.execute(
                    "UPDATE devices SET allocation_count = allocation_count -1 WHERE uuid = ?",
                    (uuid,)
                )
                return True
        return False
