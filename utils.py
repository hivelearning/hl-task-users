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
        user.pop('type')
        user['profile'] = profile_list

    return users

def insert_listing_meta():
    """
    add in pagination template
    :param users:
    :return:
    """
    return { "cursor": "string", "next_cursor": "string"}

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

