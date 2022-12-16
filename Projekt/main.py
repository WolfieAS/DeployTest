from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
import psycopg2
from DBOperations import DBQueries as db


app = Flask(__name__)

@app.route('/')
def index():
    return "Starting Page"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['psw']      #Hier muss das passwort noch geprueft werden
        
        #pruefung DB
        #erstellung der User Session
        return redirect(url_for('mainmenu'))

    users = db.getAllUsers()
    return render_template('login.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    users = db.addUser("name1", "password1", "email1")
    return render_template('login.html')

@app.route('/mainmenu', methods=['GET', 'POST'])
def mainmenu():
    #Pruefung der User Session, ansonsten /login
    return render_template('mainmenu.html')


if __name__ == '__main__':
    app.run(debug=True)