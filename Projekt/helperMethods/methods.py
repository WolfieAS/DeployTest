from DBOperations import DBQueries as db
import bcrypt
from DBOperations.DBQueries import getUser

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