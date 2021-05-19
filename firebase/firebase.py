import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import dotenv
import os
import sys
import base64
import json

dotenv.load_dotenv()

creds = json.loads(base64.b64decode(os.environ['CREDS'].encode('ascii')).decode('ascii'))

cred = credentials.Certificate(creds)
firebase_admin.initialize_app(cred)
print(str(cred))

db = firestore.client()
