from flask import Flask, request, jsonify, abort, make_response
from db_actions import get_db, insert_user, search_user_by_id, user_exists, remove_user, update_user, search_donors
from utils import filter_users, format_users, insert_listing_meta, extract_profile, sort_users_by_country
from validations import validate_request_body
import copy
  
app = Flask(__name__) 

@app.route('/', methods=['GET'])
def list_users():
    """
    Get users and profiles
    :return:
    """
    data = get_db()
 
    users = filter_users(data, request.args)
    profiles = [x for x in data if (x['type'] == 'profile')]
    result = format_users(users, profiles)

    return jsonify({'data': result, 'meta': insert_listing_meta()})

@app.route('/', methods=['POST'])
def create_user():
    """
    Create single user
    :return:
    """        
    user = request.json
    response = copy.deepcopy(user)

    validate_request_body(user, 'POST')
    insert_user(user) 

    return jsonify(response), 201

@app.route('/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Get user by id
    :param user_id:
    :return:
    """    
    user = search_user_by_id(user_id) 
    if not user:
        abort(404)  

    return jsonify({'data': user, 'meta': insert_listing_meta()})
 
@app.route('/<string:user_id>', methods=['PUT'])
def replace_user(user_id):
    """
    replace user,
    (!) the id's of profile fields are newly created
    :param user_id:
    :return:
    """
    user = request.json

    validate_request_body(user, 'PUT')
    
    if not user_exists(user_id):
        abort(404)
    
    remove_user(user_id)
    insert_user(user) 

    return jsonify({'Success' : '204'}), 204

@app.route('/<string:user_id>', methods=['PATCH'])
def patch_user(user_id):
    """
    update user
    :param user_id:
    :return:
    """
    body = request.json
    validate_request_body(body, 'PATCH')

    if not user_exists(user_id):
        abort(404)
    
    update_user(user_id, body)

    return jsonify({'Success' : '204'}), 204

@app.route('/<string:user_id>/donors', methods=['GET'])
def get_donors(user_id):
    """
    steps
    get user
    get blood_group
    get compatible donors by user_id
    get users
    sort users by country
    :param user_id:
    :return:
    """

    #get_user
    user = search_user_by_id(user_id)
    if not user:
        abort(404)

    profile = extract_profile(user)
 
    #get blood_group
    blood_group = [x['value'] for x in profile if x['field'] == 'blood_group']    
    if not blood_group:
        abort(404)

    #get user_ids
    user_ids = search_donors(blood_group[0])
   
    #remove original user 
    user_ids.remove(user_id)
    if not user_ids:
        abort(404)
    
    #get users by id
    users = [search_user_by_id(x) for x in user_ids]
    
    #sort: user's country first 
    user_country = [x['value'] for x in profile if x['field'] == 'country']
    if user_country:
        users = sort_users_by_country(users, user_country[0])

    return jsonify({'data': users, 'meta': insert_listing_meta()})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not Found'}),404)

@app.errorhandler(400)
def request_invalid(error):
    return make_response(jsonify({'error' : 'Request Invalid'}),400)

if __name__ == '__main__':
    app.run(debug=True) 