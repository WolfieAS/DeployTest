import psycopg2
from _datetime import date
from locale import str
from datetime import datetime
import bcrypt
import uuid
import pyqrcode
from PIL import Image
from flask import jsonify


class User:
    id: int
    password: str
    email: str
    usertype: int
    responsible_for: str
    firstname: str
    lastname: str
    birthdate: date
    zipcode: str
    street: str
    city: str
    country: str
    phone: str


    def __init__(self, id, email, pw, type, responsible, first, last, dob, zip, street, city, country, phone):
        self.id = id
        self.email = email
        self.password = pw
        self.usertype = type
        self.responsible_for = responsible
        self.firstname = first
        self.lastname = last
        self.birthdate = dob
        self.zip = zip
        self.street = street
        self.city = city
        self.country = country
        self.phone = phone


class Ticket:
    serial_id: str
    user_id: int
    ticket_id: int
    firstname: str
    lastname: str
    birthdate: date
    valid_from: datetime
    valid_to: datetime

    def __init__(self, serial_id, user_id, ticket_id, firstname, lastname, dob, valid_from, valid_to):
        self.serial_id = serial_id
        self.user_id = user_id
        self.ticket_id = ticket_id
        self.firstname = firstname
        self.lastname = lastname
        self.dob = dob
        self.valid_from = valid_from
        self.valid_to = valid_to

def userFromDB(dbOut):
    for item in dbOut:
        if item is None:
            item = ""
    return User(dbOut[0], dbOut[1], dbOut[2], dbOut[3], dbOut[4], dbOut[5], dbOut[6], dbOut[7], dbOut[8], dbOut[9], dbOut[10], dbOut[11], dbOut[12])


def checkUser(username, password):
    user = getUser(username)
    user = userFromDB(user[0])
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return True, user
    else:
        return False, None


def hashPassword(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def generateUUID():
    myuuid = uuid.uuid4()
    myuuid = str(myuuid)
    myuuid = myuuid.replace("-", "")
    return myuuid


def createQRCode(serial_no):
    input_data = "http://127.0.0.1:5000/mytickets/" + str(serial_no)

    url = pyqrcode.QRCode(input_data, error='H')
    url.png('./Photos/qr.jpg', scale=10)
    im = Image.open('./Photos/qr.jpg')
    im = im.convert("RGBA")
    logo = Image.open('./Photos/logo.jpg')
    box = (135, 135, 265, 265)
    im.crop(box)
    region = logo
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    im.paste(region, box)
    return (im)
    # im.show()
    # os.remove("./Photos/qr.jpg")


def checkSerial_no(serial_no):
    try:
        dbserial_no = checkTicket(serial_no)
        dbserial_no = [i[0] for i in dbserial_no]
        dbserial_no = ''.join([str(elem) for elem in dbserial_no[0]])
        print(dbserial_no)
        if (dbserial_no == serial_no):
            return True
    except IndexError:
        return False


def groupTickets(ticket, redeemed_tickets):
    for i in range(len(ticket)):
        for x in range(len(redeemed_tickets)):
            if ticket[i][8] == redeemed_tickets[x][1]:
                used_on = redeemed_tickets[x][2]
                used_at = redeemed_tickets[x][3]
                ticket[i] = ticket[i] + (used_on, used_at,)
        print(ticket[i])
    return ticket


def connection():
    conn = psycopg2.connect("postgres://mcrowrwh:xEsjLVGphy09Q47wKhMvjcg1hOkGLgrD@rogue.db.elephantsql.com/mcrowrwh")
    return conn


def getAllUsers():
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    conn.commit()
    result = (cur.fetchall())
    cur.close()
    conn.close()
    return result


def getUser(username):
    conn = connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, email, password, usertype, responsible_for, firstname, lastname, birthdate, zipcode, street, city, country, phonenumber FROM users WHERE email=%s",
        (username,))
    conn.commit()
    result = (cur.fetchall())
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
    result = (cur.fetchall())
    cur.close()
    conn.close()
    return result


def getAllTicketsFromUser(user_id):
    conn = connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM ticket RIGHT JOIN registrated_tickets r ON ticket.ticket_id =r.ticket_id WHERE r.user_id=%s",
        (user_id,))
    conn.commit()
    result = (cur.fetchall())
    cur.close()
    conn.close()
    return result


def registrateTicket(serial_no, user_id, ticket_id):
    conn = connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO registrated_tickets (serial_no, user_id, ticket_id) VALUES (%s, %s, %s)",
                (serial_no, user_id, ticket_id))
    conn.commit()
    cur.close()
    conn.close()


def addTicket(name: str, valid_from: date, valid_to: date, returnable: bool, amount: int, price: int, location: str):
    conn = connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ticket (name, valid_from, valid_to, returnable, amount, price, location) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (name, valid_from, valid_to, returnable, amount, price, location))
    conn.commit()
    cur.close()
    conn.close()


def checkTicket(serial_no):
    conn = connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM registrated_tickets RT INNER JOIN ticket T ON RT.ticket_id=T.ticket_id WHERE RT.serial_no =%s",
        (serial_no,))
    conn.commit()
    result = (cur.fetchall())
    cur.close()
    conn.close()
    return result


def reedem_ticket(serial_no, used_on):
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO redeemed_tickets(serial_no, used_on, used_at) VALUES(%s, %s, %s)",
                (serial_no, used_on, today,))
    conn.commit()
    cur.close()
    conn.close()


def getUser_redeemed_tickets(user_id):
    conn = connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM redeemed_tickets RED INNER JOIN registrated_tickets REG ON REG.serial_no = RED.serial_no WHERE REG.user_id=%s",
        (user_id,))
    conn.commit()
    result = (cur.fetchall())
    cur.close()
    conn.close()
    return result


def updatePasswort(username, password):
    conn = connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=%s WHERE username=%s", (password, username,))
    conn.commit()
    result = (cur.fetchall())
    cur.close()
    conn.close()
    return result