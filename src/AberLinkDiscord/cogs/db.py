"""Provides functions to connect to PostgreSQL database

connect() connects to database
try_connection() attempts to get cursor otherwise calls database connection again
get_discord_user() gets discord user information
get_openid_user() gets openID Connect (Aberystwyth) user data
get_discord_accounts() returns JSON array of all linked Discord accounts to an OpenID Connect account
get_connection_status() gets connection status on database. e.g. is working or is free
get_polling_status() gets polling information on database
get_connection_latency() gets the database latency
"""

__author__ = "Joel Adams"
__maintainer__ = "Joel Adams"
__email__ = "joa38@aber.ac.uk"
__version__ = "2.0"
__status__ = "Production"
__system__ = "Discord bot"
__deprecated__ = False

import os
import psycopg2
from psycopg2 import extensions
from dotenv import load_dotenv, find_dotenv
from time import time

# Initialises a global variarable for the connection
CONN = 0

class PostgreSQL():
    """
    Responsible for database interactions
    """

    def connect():
        """
        Connects or reconnects to database
        """
        load_dotenv(find_dotenv())
        DB_NAME = os.getenv('DATABASE_NAME')
        DB_USER = os.getenv('USER')
        DB_PASSWORD = os.getenv('PASSWORD')
        DB_HOST = os.getenv('HOST')
        DB_PORT = os.getenv('PORT')

        try:
            global CONN
            CONN = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            print(f'Reconnected to PSQL database: {CONN}')
        except psycopg2.OperationalError as err:
            print(f'Error connecting to database. Error: {err}')
            raise
    

    def try_connection():
        """
        Attempts to get a cursor from the database otherwise it restarts the database connection
        """
        try:
            CONN.cursor()
        except psycopg2.InterfaceError:
            PostgreSQL.connect()


    def get_discord_user(discord_id: int):
        """ 
        Returns a discord user if they exist or None
        """
        PostgreSQL.try_connection()
        cur = CONN.cursor()

        cur.execute(f"SELECT * FROM login_discorduser WHERE id={discord_id}")
        row = cur.fetchone()
        if row is not None:
            return {"id": row[0], "last_login": row[1], "openidc_id": row[2]}


    def get_openid_user(openidc_id: int):
        """ 
        Returns a openid user if they exist or None
        """
        PostgreSQL.try_connection()
        cur = CONN.cursor()

        cur.execute(f"SELECT * FROM login_openidcuser WHERE id={openidc_id}")
        row = cur.fetchone()
        if row is not None:
            return {"id": row[0], "username": row[1], "name": row[2], "email": row[3], "usertype": row[4], "last_login": row[5], "is_active": row[6], "is_admin": row[7]}

    def get_discord_accounts(openid_id: int):
        """
        Returns all the discord accounts that are linked to a aber account
        e.g. {0: {"id": 1234153153152, "last_login": <datetime>, "openidc_id": 12}, 1: {"id": 6172675345676, "last_login": <datetime>, "openidc_id": 12}}
        """
        PostgreSQL.try_connection()
        cur = CONN.cursor()

        cur.execute(f"SELECT * FROM login_discorduser WHERE openidc_id={openid_id}")
        rows = cur.fetchall()
        accounts = {}
        for index, row in enumerate(rows):
            accounts.update({ index : {"id": row[0], "last_login": row[1], "openidc_id": row[2]}})
        return accounts


    def get_connection_status():
        """
        Gets the database's connection status
        Returns either 🟢 (database fine), 🟠 (database is doing something)
        """
        PostgreSQL.try_connection()
        db_status = CONN.status()

        # evaluate the status for the PostgreSQL connection
        if db_status == extensions.STATUS_READY:
            # psycopg2 status 1: Connection is ready for a transaction
            return '🟢 STATUS_READY'
        elif db_status == extensions.STATUS_BEGIN:
            # psycopg2 status 2: An open transaction is in process
            return '🟠 STATUS_BEGIN'
        elif db_status == extensions.STATUS_IN_TRANSACTION:
            # psycopg2 status 3: An exception has occured
            return '🟠 STATUS_IN_TRANSACTION'
        elif db_status == extensions.STATUS_PREPARED:
            # psycopg2 status 4: A transcation is in the 2nd phase of the process
            return '🟠 STATUS_PREPARED'


    def get_polling_status():
        """
        Gets the database's polling status (checks what state the database is in)
        Returns either 🟢 POLL_OK, 🟠 POLL_READ, 🟠 POLL_WRITE
        """
        PostgreSQL.try_connection()
        poll = CONN.poll()

        if poll == extensions.POLL_OK:
            return '🟢 POLL_OK'
        elif poll == extensions.POLL_READ:
            return '🟠 POLL_READ'
        elif poll == extensions.POLL_WRITE:
            return '🟠 POLL_WRITE'


    def get_connection_latency():
        """
        Returns the latency of the database connection in ms
        """
        start_time = time()

        PostgreSQL.try_connection()
        cur = CONN.cursor()

        cur.execute("SELECT * FROM login_openidcuser")
        end_time = time()
        return int((end_time - start_time) * 1000)

