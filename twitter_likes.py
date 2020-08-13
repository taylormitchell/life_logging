import os
import requests
import json
import secrets

DB_PATH = os.path.expanduser("~/GoogleDrive/logs/twitter_likes.json")
endpoint = "https://api.twitter.com/1.1/favorites/list.json?count=200&screen_name=tiptoptm"
headers = {"Authorization": f"Bearer {secrets.TWITTER_BEARER}"}


class Db:
    def __init__(self, filepath=DB_PATH):
        self.filepath = filepath
        self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            self.docs = []
        else:
            with open(self.filepath) as f:
                self.docs = json.load(f)

    def get(self, id):
        for doc in self.docs:
            if doc['id']==id:
                return doc

    def insert_one(self, doc, overwrite=False):
        for i, saved_doc in enumerate(self.docs):
            if saved_doc['id']==doc['id'] and overwrite:
                self.docs[i] = doc
                return
        self.docs.append(doc)

    def insert_many(self, docs):
        if not self.docs:
            self.docs = docs
        else:
            raise NotImplementedError

    def append(self, doc):
        self.docs.append(doc)

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.docs, f, indent=4)

def init():
    if os.path.exists(self.filepath):
        raise ValueError("db already exists") 
    db = Db()
    res = requests.get(endpoint, headers=headers).json()
    db.insert_many(res)
    db.save()

def update():
    # TODO
    pass

if __name__=="__main__":
    db = Db()
    import pandas as pd
    created_at = pd.Series([doc["created_at"] for doc in db.docs])
    print(created_at.is_monotonic_decreasing)
    created_at = pd.to_datetime(created_at)
    print(created_at.is_monotonic_decreasing)
    import pdb; pdb.set_trace()





