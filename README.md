Users API task
==================

The aim of this exercise is to build a small API around the data
structures provided using Python 3. The API should as a minimum provide
the functionality to conform with the swagger file included in the repo.

The swagger.yml file in the root of this repo describes the required
API endpoints. You can view it in a UI by
[pasting into this form](https://editor.swagger.io).

You should clone this repository, and make your submission in the form
of a Pull Request.


Setting up data
---------------

There is an [TinyDB](https://tinydb.readthedocs.io) database to be
populated with fake user data; a small 10-user [sample file](sample.json)
is included for reference. To initialise the full database:

Setup your virtual environment to use Python 3, for instance
```
virtualenv -p /usr/local/bin/python3 venv
source venv/bin/activate
```

Then install requirements, and run the init command:

```
pip install -r requirements.txt
python setup/create_user_data.py -u {number of users}
```

You should now have a database with - by default - 1000 users and
their associated profiles populated. To reset and generate new data,
simply remove the `hdata.json` file from the repo directory and re-run
the above setup command.

You can test that the database is populated by running the command
`python api.py --path "/countries"`

Requirements
------------

 - The API should be accessible either via an HTTP endpoint on localhost
e.g. `curl -X GET http://localhost:8181/`, or by
invoking functions directly e.g. `python api.py --method "GET" --path "/"`
 - Code must be in Python
 - Any additional dependencies should be added to the `requirements.txt`
file, and if applicable any setup instructions provided


What we are looking for
-----------------------

 - High quality, maintainable code
 - Sensible separation of functionality
 - Atomic commits, with meaningful commit messages
 - Test cases for the code
