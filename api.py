import argparse
from tinydb import TinyDB, Query

db = TinyDB('hdata.json')

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--method', type=str, help='method', default='GET')
parser.add_argument('-p', '--path', type=str, help='path', default='/')
args = parser.parse_args()


def list_users():
    """
    Sample query listing all users
    :return:
    """
    for row in db.search(Query().type == 'user'):
        print(row)


def list_user_countries():
    """
    Sample query listing all countries users are found in
    :return:
    """
    profile = Query()
    countries = set()
    for row in db.search((profile.type == 'profile') & (profile.field == 'country')):
        countries.add(row['value'])

    print(sorted(list(countries)))


if args.path == '/':
    list_users()
elif args.path == '/countries':
    list_user_countries()