import json
import os

import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreDatabase():

    _db = None

    def __new__(cls):
        if not cls._db:
            firebase_credentials = json.loads(os.environ['FIREBASE_CREDENTIALS'])
            firebase_admin.initialize_app(credential=credentials.Certificate(firebase_credentials))

            cls._db = firestore.client()

        return cls._db


db = FirestoreDatabase()
