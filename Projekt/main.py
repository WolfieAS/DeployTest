from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
import psycopg2
import bcrypt
from DBOperations import DBQueries as db
from helperMethods import methods


app = Flask(__name__)

@app.route('/')
def index():
    return "Starting Page"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['psw']
              
        if(methods.checkUser(username, password)):
            #create session
            return redirect(url_for('mainmenu'))
        else:
            return redirect(url_for('login'))
            
             
    users = db.getAllUsers()
    return render_template('login.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():   
    if request.method == "POST":
        username = request.form['uname']
        email = request.form['email']
        password = request.form['psw']
        #Validity check
        password = methods.hashPassword(password) # Hash password
        db.addUser(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/mainmenu', methods=['GET', 'POST'])
def mainmenu():
    #Pruefung der User Session, ansonsten /login
    return render_template('mainmenu.html')


if __name__ == '__main__':
    app.run(debug=True)