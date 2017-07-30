from contextlib import contextmanager
from subprocess import Popen, PIPE
from urllib.parse import urlparse

import psycopg2
import pytest
from psycopg2 import pool

from app import settings
from app.main import application

db_param = urlparse(settings.DATABASE_URL)
TEST_DB = db_param.path[1:]
TEST_USER = db_param.username
TEST_PWD = db_param.password
TEST_HOST = db_param.hostname


@pytest.fixture(scope='session')
def app():
    """
    Application fixture
    Required by pytest-tornado
    """
    return application


@pytest.fixture(scope='session', autouse=True)
def fix_db(request):
    """
    Database fixture
    Creates Postgresql test database and applies yoyo migrations
    Drops database on teardown
    """
    # Create database
    with psycopg2.connect(
            'host={0} dbname=postgres user={1} password={2}'.format(TEST_HOST, TEST_USER, TEST_PWD)
    ) as conn:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute('CREATE DATABASE %s' % TEST_DB)
    # Start django migrations
    command = "yoyo apply --database {} ./migrations/migrations -b".format(settings.DATABASE_URL)
    proc = Popen(
        command.split(),
        stdout=PIPE, stderr=PIPE
    )
    proc.communicate()

    def teardown():
        # Opened connections should be terminated before dropping database
        terminate_sql = "SELECT pg_terminate_backend(pg_stat_activity.pid) " \
                        "FROM pg_stat_activity " \
                        "WHERE pg_stat_activity.datname = %s " \
                        "AND pid <> pg_backend_pid();"
        with psycopg2.connect(
                'host={0} dbname=postgres user={1} password={2}'.format(TEST_HOST, TEST_USER, TEST_PWD)) as conn:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as cur:
                cur.execute(terminate_sql, (TEST_DB,))
                cur.execute('DROP DATABASE %s' % TEST_DB)

    request.addfinalizer(teardown)
    db = pool.SimpleConnectionPool(
        14, 14, host=TEST_HOST, database=TEST_DB, user=TEST_USER, password=TEST_PWD, port=5432
    )

    @contextmanager
    def get_cursor():
        con = db.getconn()
        try:
            yield con.cursor()
            con.commit()
        finally:
            db.putconn(con)

    return get_cursor


@pytest.fixture()
def clean_table(request, fix_db):
    """
    This fixture should be used only with
    request.param set to iterable with subclasses of peewee.Model or single peewee.Model
    It clears all data in request.param table
    Usage:
    @pytest.mark.parametrize('clean_table', [(Log, Route)], indirect=True)
    """

    def teardown():
        # with async_db.getconn() as connection:
        #     with connection.cursor() as cur:
        with fix_db() as cur:
            for param in request.param:
                cur.execute('delete from %s;' % param)

    request.addfinalizer(teardown)
