import psycopg2

def connection():
    conn = psycopg2.connect("postgres://mcrowrwh:xEsjLVGphy09Q47wKhMvjcg1hOkGLgrD@rogue.db.elephantsql.com/mcrowrwh")
    return conn

def getAllUsers():
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    conn.commit()
    result=(cur.fetchall())
    cur.close()
    conn.close()
    return result

def addUser(username, password, email):
    conn = connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
    conn.commit()
    cur.close()
    conn.close()