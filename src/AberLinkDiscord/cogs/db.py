from psycopg2 import extensions
from AberLink import conn
from time import time

class PostgreSQL():
    """
    Responsible for database interactions
    """


    def get_discord_user(discord_id: int):
        """ 
        Returns a discord user if they exist or None
        """
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM login_discorduser WHERE id={discord_id}")
        row = cur.fetchone()
        if row is not None:
            return {"id": row[0], "last_login": row[1], "openidc_id": row[2]}


    def get_openid_user(openidc_id: int):
        """ 
        Returns a openid user if they exist or None
        """
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM login_openidcuser WHERE id={openidc_id}")
        row = cur.fetchone()
        if row is not None:
            return {"id": row[0], "username": row[1], "name": row[2], "email": row[3], "usertype": row[4], "last_login": row[5], "is_active": row[6], "is_admin": row[7]}


    def get_connection_status():
        """
        Gets the database's connection status
        Returns either 🟢 (database fine), 🔴 (connection lost), 🟠 (database is doing something)
        """
        db_status = conn.status
        # evaluate the status for the PostgreSQL connection
        if db_status == extensions.STATUS_READY:
            # psycopg2 status 1: Connection is ready for a transaction
            return '🟢 STATUS_READY'
        elif db_status == extensions.STATUS_BEGIN:
            # psycopg2 status 2: An open transaction is in process
            return '🟠 STATUS_BEGIN'
        elif db_status == extensions.STATUS_IN_TRANSACTION:
            # psycopg2 status 3: An exception has occured
            return '🔴 STATUS_IN_TRANSACTION'
        elif db_status == extensions.STATUS_PREPARED:
            # psycopg2 status 4: A transcation is in the 2nd phase of the process
            return '🟠 STATUS_PREPARED'


    def get_polling_status():
        """
        Gets the database's polling status (checks what state the database is in)
        Returns either 🟢 POLL_OK, 🟠 POLL_READ, 🟠 POLL_WRITE
        """
        if conn.poll() == extensions.POLL_OK:
            return '🟢 POLL_OK'
        if conn.poll() == extensions.POLL_READ:
            return '🟠 POLL_READ'
        if conn.poll() == extensions.POLL_WRITE:
            return '🟠 POLL_WRITE'


    def get_connection_latency():
        """
        Returns the latency of the database connection in ms
        """
        start_time = time()
        cur = conn.cursor()
        cur.execute("SELECT * FROM login_openidcuser")
        end_time = time()
        return int((end_time - start_time) * 1000)

