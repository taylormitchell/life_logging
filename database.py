import os
import sqlite3
import logging

class Db:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.last_columns = None

    def execute(self, cmd):
        c = self.conn.cursor()
        try:
            c.execute(cmd)
        finally:
            c.close()

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
    db = Db("temp.sqlite")
    with open("schemas/roam.txt") as f:
        cmd = f.read()
    db.execute(cmd)