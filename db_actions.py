from tinydb import TinyDB, Query, where
from utils import format_users
import uuid

DB_NAME = 'hdata.json'
db = TinyDB(DB_NAME)
 
def get_db():
    return db.all()
