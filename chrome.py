import os
import sqlite3
from shutil import copyfile
import logging

class Db:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.last_columns = None

    def fetchall(self, cmd):
        c = self.conn.cursor()
        try:
            c.execute(cmd)
            records = c.fetchall()
            self.last_columns = self._get_columns(c)
        finally:
            c.close()
        return records

    def fetchone(self, cmd):
        c = self.conn.cursor()
        try:
            c.execute(cmd)
            records = c.fetchone()
            self.last_columns = self._get_columns(c)
        finally:
            c.close()
        return records

    def insert(self, table, records, columns=None):
        if not records:
            return

        table = table if not columns else table + "(%s)" % ','.join(columns)
        wildcards = "(%s)" % ','.join(["?"]*len(records[0]))
        cmd = f"INSERT OR IGNORE INTO {table} VALUES {wildcards}"

        c = self.conn.cursor()
        try:
            c.executemany(cmd, records)
            self.conn.commit()
        finally:
            c.close()

    def _get_columns(self, cursor):
        return [t[0] for t in cursor.description]


if __name__=="__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    history_src = "~/Library/Application Support/Google/Chrome/Default/History"
    history_copy = "temp"
    copyfile(os.path.expanduser(history_src), history_copy)

    # Make a temp copy of History cause it's most likely locked
    chrome_db = Db(history_copy)
    my_db = Db(os.path.expanduser("~/GoogleDrive/logs/chrome.sqlite"))

    table_and_id = [
        ('urls','id'),
        ('visits','id'),
        ('visit_source','id'),
        ('downloads','id'),
        ('downloads_url_chains','id'),
        ('downloads_slices','download_id'),
        ('segments','id'),
        ('segment_usage','id'),
        ('keyword_search_terms','url_id')]
    for table, col_id in table_and_id:
        max_chrome_id = chrome_db.fetchone(f"select max({col_id}) from {table}")[0] or -1
        max_my_id = my_db.fetchone(f"select max({col_id}) from {table}")[0] or -1
        # If the id is smaller than the History table must've reset of something.
        # This means the id columns between the databases won't be in sync anymore.
        if max_chrome_id < max_my_id:
            raise ValueError(f"History id got smaller in {table}")

        # Copy records over
        records = chrome_db.fetchall(f"""
            select * from {table} 
            where {col_id} > {max_my_id}""")
        my_db.insert(table, records)

    os.remove(history_copy)
    logging.info("Chrome history successfully synced")
        
