from tinydb import TinyDB, Query, where
from utils import format_users
import uuid

DB_NAME = 'hdata.json'
db = TinyDB(DB_NAME)
 
def get_db():
    return db.all()
 
def insert_user(user_data):
    """
    Insert user data
    :param user_id:
    :param profile_data:
    :return:
    """    
    result = user_data
    user_data['type'] = 'user'
    for profile in user_data['profile']:
        insert_profile(profile)
        
    user_data.pop('profile')
    db.insert(user_data)
    return result

def insert_profile(profile):
    """
    Insert profile data into table
    :param user_id:
    :param profile_data:
    :return:
    """
    fields = []
    fields.append({'type': 'profile', 'id': str(uuid.uuid4()),'user_id': profile.get('user_id', None), 'field': profile.get('field', None), 'value': profile.get('value', None)})
    db.insert_multiple(fields)
    return profile

def search_user_by_id(user_id):
    Users = Query()
    user = db.search((Users.type == 'user') & (Users.id == user_id))
    profiles = db.search((Users.type == 'profile') & (Users.user_id == user_id))
    user = format_users(user, profiles)
    return user