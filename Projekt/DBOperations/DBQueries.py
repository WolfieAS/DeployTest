import psycopg2
from _datetime import date
from locale import str
from test.test_functools import decimal

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

def getUser(username):
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM users WHERE username=%s", (username,))
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

def getAllTickets():
    
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ticket")
    conn.commit()
    result=(cur.fetchall())
    cur.close()
    conn.close()
    return result

def registrateTicket(user_id, ticket_id):

    conn = connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO registrated_tickets (user_id, ticket_id) VALUES (%s, %s)", (user_id, ticket_id))
    conn.commit()
    cur.close()
    conn.close()

def addTicket(name:str, valid_from: date, valid_to: date, returnable:bool, amount:decimal, price:decimal, location:str):
    
    conn = connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO ticket (name, valid_from, valid_to, returnable, amount, price, location) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, valid_from, valid_to, returnable, amount, price, location))
    conn.commit()
    cur.close()
    conn.close()
    
def checkTicket(serial_no):
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM registrated_tickets WHERE serial_no=%s", (serial_no,))
    conn.commit()
    result=(cur.fetchall())
    cur.close()
    conn.close()
    return result