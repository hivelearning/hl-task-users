from flask import abort

def filter_users(data, args):
    """
    Filter users, returns users
    :param data, args
    :return:
    """    
    user_ids = []
 
    if not args:
        users = [x for x in data if (x['type'] =='user')]
    else:
        for k in args:
            value = args.get(k)
            user_ids = filter_on_arg(data, user_ids, value)
            if not user_ids:
                abort(404)
        users = [x for x in data if ((x['type'] == 'user') & (x['id'] in user_ids))]

    return users

def filter_on_arg(data, user_ids, value):
    """
    filter per argument
    :params data, user_ids value:
    :return li userids:
    """
    ids_list = [x['user_id'] for x in data if (x['type'] == 'profile' and x['value'] == value)]
    if not ids_list:
        return
    if len(user_ids) != 0:
        user_ids = intersection(user_ids, ids_list)
    else: 
        user_ids = ids_list

    return user_ids    

def intersection(list1, list2):
    """
    Finds common values
    :params list1, list2
    :return:
    """
    list_r = [value for value in list1 if value in list2]
    return list_r

def format_users(users, profiles):
    """
    formats users
    :params users, profiles
    :return:
    """
    for user in users:
        profile_list = create_profile_list(user, profiles)
        user['profile'] = profile_list
        if 'type' in user:
            user.pop('type')

    return users

def create_profile_list(user, profiles):
    """
    formats list of profile fields
    :param user, profiles:
    :return:
    """
    profile_list = []
    for profile in profiles:
        if user['id'] == profile['user_id']:
            profile_list.append(profile)
    
    return profile_list

def insert_listing_meta():
    """
    add in pagination template
    :param users:
    :return:
    """
    return { "cursor": "string", "next_cursor": "string"}

def validate_key(body, key):
    """
    validates key
    :params body, string
    """
    value = body.get(key)
    if value is None:
        abort(400)

def validate_type(body, key, type_val):
    """
    validates body
    :params body, key, type:
    """
    value = body.get(key)

    if not type(value) == type_val:
        abort(400)
       
def extract_profile(user):
    """
    extract profile list from user list
    :param user:
    :return:
    """   
    return user[0]['profile']


def sort_users_by_country(user_list, key):
    """
    Sort users, with country 'key' first
    Steps:
    1 iterate over users
    2 check if same country
    3 re-order output list
    :params user_list, key:
    :return:
    """
    matching_user_ids = []
    
    for user in user_list:  
        profile_obj = user[0]
        profile = profile_obj['profile']

        user_id_same_country = [field['user_id'] for field in profile if ((field['field'] == 'country') & (field['value'] == key))]
        if user_id_same_country:
            matching_user_ids.append(user_id_same_country[0])

    result = order_output_list_by_country(user_list, matching_user_ids) if matching_user_ids else user_list
    return result

def order_output_list_by_country(user_list, matching_user_ids):
    """
    orders output with same country first
    :params user_list, matching_user_ids:
    :return:
    """
    output_list = []
    secondary_list = []
    for user in user_list:
        user_dict = user[0]

        if user_dict['id'] in matching_user_ids:
            output_list.append(user_dict)
        else:
            secondary_list.append(user_dict)
    #merge lists if secondary list
    result = [y for x in [output_list, secondary_list] for y in x] if secondary_list else output_list
    return result
