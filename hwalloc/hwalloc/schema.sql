DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS device;
CREATE TABLE device (
    uuid TEXT PRIMARY KEY UNIQUE NOT NULL,
    allocation_count INTEGER NOT NULL
);