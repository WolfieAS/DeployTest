from DBOperations import DBQueries as db
import bcrypt
import qrcode
import uuid
from DBOperations.DBQueries import getUser, reedem_ticket
import pyqrcode
from PIL import Image
import os
from dataclasses import replace

def checkUser(username, password):
    user = db.getUser(username)
    hashedPassword =  [i[1] for i in user]
    hashedPassword = ' '.join([str(elem) for elem in hashedPassword])
    
    if user and bcrypt.checkpw(password.encode('utf-8'), hashedPassword.encode('utf-8')):
        return True
    else:
        return False
   

def hashPassword(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def getUser_id(username):
    user = db.getUser(username)
    user_id =  [i[2] for i in user]
    user_id = ' '.join([str(elem) for elem in user_id])
    return user_id

def getUsertype(username):
    user = db.getUser(username)
    usertype =  [i[3] for i in user]
    usertype = ' '.join([str(elem) for elem in usertype])
    return usertype

def getResponsible_for(username):
    user = db.getUser(username)
    responsible =  [i[4] for i in user]
    responsible = ' '.join([str(elem) for elem in responsible])
    return responsible

def generateUUID():
    myuuid = uuid.uuid4()
    myuuid = str(myuuid)
    myuuid = myuuid.replace("-", "")
    return myuuid
    

def createQRCode(serial_no):
    input_data = "http://127.0.0.1:5000/mytickets/"+str(serial_no) 

    url = pyqrcode.QRCode(input_data, error = 'H')
    url.png('./Photos/qr.jpg',scale=10)
    im = Image.open('./Photos/qr.jpg')
    im = im.convert("RGBA")
    logo = Image.open('./Photos/logo.jpg')
    box = (135,135,265,265)
    im.crop(box)
    region = logo
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    im.paste(region,box)
    im.show()
    os.remove("./Photos/qr.jpg")


def checkSerial_no(serial_no):
    try:
        dbserial_no = db.checkTicket(serial_no)
        dbserial_no =  [i[0] for i in dbserial_no]
        dbserial_no = ''.join([str(elem) for elem in dbserial_no[0]])
        print(dbserial_no)
        if(dbserial_no==serial_no):
            return True
    except IndexError:
        return False
    
def groupTickets(ticket, redeemed_tickets):   
    for i in range(len(ticket)):
        for x in range(len(redeemed_tickets)):
            if ticket[i][8] == redeemed_tickets[x][1]:
                used_on = redeemed_tickets[x][2]
                used_at = redeemed_tickets[x][3]
                ticket[i] = ticket[i]+(used_on, used_at, )
        print(ticket[i])
    return ticket
        

    