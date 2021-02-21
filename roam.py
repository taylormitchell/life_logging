import json
import logging
import sqlite3
import os

MASTER = os.path.expanduser("~/GoogleDrive/logs/master.sqlite")
ROAM_JSON = os.path.expanduser("~/GitHub/roam_backup/json/second_brain.json")
ROAM_TABLE = "roam"
SCHEMA = f"""
CREATE TABLE IF NOT EXISTS {ROAM_TABLE} (
    uid             TEXT        PRIMARY KEY,
    create_time     INTEGER,
    edit_time       INTEGER,
    create_email    TEXT,
    edit_email      TEXT,
    string          TEXT
);
"""

def create_table():
    conn = sqlite3.connect(MASTER)
    curs = conn.cursor()
    try:
        curs.execute(SCHEMA)
    finally:
        curs.close()

def upload_block(block, curs):
    # Get data
    columns = [
        "uid",
        "create-time", 
        "edit-time",
        "create-email",
        "edit-email",
        "string"
    ]
    values = [block.get(c) for c in columns]
    columns = [c.replace("-","_") for c in columns]

    # Upload to database
    cmd = f"""
    INSERT OR REPLACE INTO 
    {ROAM_TABLE}({','.join(columns)})
    VALUES ({','.join(['?']*len(columns))})"""
    curs.executemany(cmd, [values])

    # Upload children to dabase
    for child in block.get("children",[]):
        upload_block(child, curs)

def update_table():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    with open(ROAM_JSON) as f:
        pages = json.load(f)

    conn = sqlite3.connect(MASTER)
    curs = conn.cursor()
    try:
        for page in pages:
            for block in page.get("children",[]):
                upload_block(block, curs)
        conn.commit()
    finally:
        curs.close()

    conn.close()
    logging.info("Roam successfully synced")

if __name__=="__main__":
    create_table()
    update_table()
