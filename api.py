from flask import Flask, request, jsonify, abort, make_response
from db_actions import get_db
from utils import filter_users, format_users, insert_listing_meta

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

if __name__ == '__main__':
    app.run(debug=True) 