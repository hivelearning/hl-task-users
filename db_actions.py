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

def remove_user(user_id):
    """
    Remove user
    :param user:
    """
    db.remove(where('user_id') == user_id)
    db.remove(where('id') == user_id)

def user_exists(user_id):
    """
    User exists
    :param user_id:
    :return:
    """
    return db.contains((Query().type == 'user') & (Query().id == user_id))

def update_profile_fields(profile_fields, user_id):
    """
    update profile field in db
    :param profile_fields:
    """
    User = Query()
    profile_db = db.search((User.type == 'profile') & (User.user_id == user_id))

    for field in profile_db:
        for profile_field in profile_fields:
            if field['field'] == profile_field['field']: 
                field['value'] = profile_field['value'] 

    db.write_back(profile_db)
    
def update_user_field(key, value, user_id):
    """
    update user fields
    :param user
    """
    User = Query()    
    user_db = db.search((User.type == 'user') & (User.id == user_id))

    for user in user_db:
        if key in user:
            user[key] = value

    db.write_back(user_db)

def update_user(user_id, body):
    """
    updates user
    :param user_id, body:
    """
    for key, value in body.items():
        if key == 'profile':
            update_profile_fields(value, user_id)
        else:
            update_user_field(key, value, user_id)
            
def search_donors(blood_group):
    """
    search donors db
    :param blood_group:
    :return list of user ids:
    """
    User = Query()
    user_profiles = db.search((User.type == 'profile') & (User.field == 'blood_group') & (User.value == blood_group))
    user_id_list = [x['user_id'] for x in user_profiles]
    
    return user_id_list
