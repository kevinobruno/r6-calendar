import json
import os

from app.core.parameter_store import ParameterStore

import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreDatabase():

    _db = None

    def __new__(cls):
        if not cls._db:
            parameter_store = ParameterStore()
            firebase_credentials = json.loads(parameter_store.get(name='FIREBASE_CREDENTIALS'))
            firebase_admin.initialize_app(credential=credentials.Certificate(firebase_credentials))

            cls._db = firestore.client()

        return cls._db


db = FirestoreDatabase()
