from DBOperations import DBQueries as db
import bcrypt
import qrcode
import uuid
from DBOperations.DBQueries import getUser
import pyqrcode
from PIL import Image
import os

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

def generateUUID():
    myuuid = uuid.uuid4()
    return str(myuuid)

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
        dbserial_no = ' '.join([str(elem) for elem in dbserial_no[0]])
        if(dbserial_no==serial_no):
            return True
    except IndexError:
        return False