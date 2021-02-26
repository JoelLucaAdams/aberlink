from AberLink import con

class PostgreSQL():

    def get_discord_user(discord_id: int):
        cur = con.cursor()
        cur.execute(f"SELECT * FROM login_discorduser WHERE id={discord_id}")
        row = cur.fetchone()
        if row is not None:
            return {"id": row[0], "last_login": row[1], "openidc_id": row[2]}

    def get_openid_user(openidc_id: int):
        cur = con.cursor()
        cur.execute(f"SELECT * FROM login_openidcuser WHERE id={openidc_id}")
        row = cur.fetchone()
        if row is not None:
            return {"id": row[0], "username": row[1], "name": row[2], "email": row[3], "usertype": row[4], "last_login": row[5], "is_active": row[6], "is_admin": row[7]}
