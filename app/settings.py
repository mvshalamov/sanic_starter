import os

from distutils.util import strtobool


DEBUG = strtobool(os.environ.get('DEBUG', 'false'))

VERSION = '0.1.0'

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://user:dbpass@pg/db')
# if postgres configure as master-slave
DATABASE_URL_READ = os.environ.get('DATABASE_URL_READ', 'postgres://user:dbpass@pg/db')
DATABASE_IMPORT_URL = os.environ.get(
    'DATABASE_IMPORT_URL',
    'postgres://import_user:import_superpass@pgsql2.prod.import.sber/import_db'
)

DATABASE_URL_TEST = os.environ.get(
    'DATABASE_URL_TEST',
    'postgres://user:dbpass@pg/test'
)

PORT = os.environ.get('PORT', 8000)

MAX_NUM_DB_CONN = os.environ.get('MAX_NUM_DB_CONN', 10)
