import psycopg2
from _datetime import date
from locale import str
from test.test_functools import decimal
from datetime import date

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
    cur.execute("SELECT username, password, user_id, usertype, responsible_for FROM users WHERE username=%s", (username,))
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

def getAllTicketsFromUser(user_id):
    
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ticket RIGHT JOIN registrated_tickets r ON ticket.ticket_id =r.ticket_id WHERE r.user_id=%s", (user_id,))
    conn.commit()
    result=(cur.fetchall())
    cur.close()
    conn.close()
    return result

def registrateTicket(serial_no, user_id, ticket_id):

    conn = connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO registrated_tickets (serial_no, user_id, ticket_id) VALUES (%s, %s, %s)", (serial_no, user_id, ticket_id))
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
    cur.execute("SELECT * FROM registrated_tickets RT INNER JOIN ticket T ON RT.ticket_id=T.ticket_id WHERE RT.serial_no =%s", (serial_no,))
    conn.commit()
    result=(cur.fetchall())
    cur.close()
    conn.close()
    return result

def reedem_ticket(serial_no, used_on):
    today = date.today()
    conn = connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO redeemed_tickets(serial_no, used_on, used_at) VALUES(%s, %s, %s)", (serial_no, used_on, today,))
    conn.commit()
    cur.close()
    conn.close()

def updatePasswort(username, password):
    conn = connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=%s WHERE username=%s", (password, username,))
    conn.commit()
    result=(cur.fetchall())
    cur.close()
    conn.close()
    return result