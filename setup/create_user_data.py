from faker import Faker
import argparse
import random
from tinydb import TinyDB, Query
import sys
import uuid

DB_NAME = 'hdata.json'
fake = Faker()
db = TinyDB(DB_NAME)


def insert_user(data):
    if type(data) == list:
        for row in data:
            row['type'] = 'user'

        db.insert_multiple(data)
    elif type(data) == dict:
        data['type'] = 'user'
        db.insert(data)


def count_users():
    """
    Retrieve a count of users
    :return:
    """
    return db.count(Query().type == 'user')


def create_sample_users(num=1000):
    """
    Adds sample set of fake users
    :param num:
    :return:
    """
    users = []
    for r in range(num):
        users.append({'id': str(uuid.uuid4()), 'firstname': fake.first_name(), 'lastname': fake.last_name()})
    insert_user(users)
    print('Users added')

    counter = 0
    for u in users:
        create_user_profile(u['id'], '{} {}'.format(u['firstname'], u['lastname']))
        counter += 1
        if counter % 25 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
    print()
    print('Profiles added')

    print('Added {} users; total count: {}'.format(num, count_users()))


def create_user_profile(user_id, name):
    """
    Adds somewhat random set of profile fields for the user
    :param user_id:
    :return:
    """
    fields = ['job', 'company', 'ssn', 'residence', 'blood_group', 'username', 'mail']
    full_profile = fake.profile(fields=fields)
    keys = random.choices(list(full_profile.keys()), k=5)

    profile_data = {k: full_profile.get(k) for k in keys}
    profile_data['name'] = name
    profile_data['city'] = fake.city()
    profile_data['country'] = fake.country()
    insert_profile_data(user_id, profile_data)
    return profile_data


def insert_profile_data(user_id: str, profile_data: dict):
    """
    Insert profile data into table
    :param user_id:
    :param profile_data:
    :return:
    """
    fields = []
    for field, value in profile_data.items():
        fields.append({'type': 'profile', 'id': str(uuid.uuid4()), 'user_id': user_id, 'field': field, 'value': value})

    db.insert_multiple(fields)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--users', type=int, nargs='?', help='The number of users to add', default=1000)
    args = parser.parse_args()

    if count_users() > 0:
        print('Database already populated; to create new data delete the file {} and re-run'.format(DB_NAME))
    else:
        num = args.users
        print('Creating {} users'.format(num))

        create_sample_users(num)
    pass
