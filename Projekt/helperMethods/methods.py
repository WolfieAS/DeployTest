from DBOperations import DBQueries as db
import bcrypt

def checkUser(username, password):
    
    return True

def hashPassword(password):
    password =password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed