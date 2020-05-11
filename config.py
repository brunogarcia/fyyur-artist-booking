import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
database_uri = 'postgresql://postgres:postgres@localhost:5432/fyyurapp'
SQLALCHEMY_DATABASE_URI = database_uri
