from DBOperations import DBQueries as db
import bcrypt
from DBOperations.DBQueries import getUser

def checkUser(username, password):
    password =password.encode('utf-8')
    user = db.getUser(username)
    hashedPassword =  [i[1] for i in user]
    hashedPassword = ' '.join([str(elem) for elem in hashedPassword])
    print(hashedPassword)
    
    if user and bcrypt.checkpw(password, hashedPassword.encode('utf-8')):
        return True
    else:
        return False
   

def hashPassword(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(hashed)
    return hashed