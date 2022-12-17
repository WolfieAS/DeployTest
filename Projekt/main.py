from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
import psycopg2
import bcrypt
from DBOperations import DBQueries as db
from helperMethods import methods


app = Flask(__name__)
app.secret_key="hello"

@app.route('/')
def index():
    tickets = db.getAllTickets()
    if "user" in session:
        user = session['user']
        return render_template('index.html', tickets=tickets, username=user)
    else:
        return render_template('index.html', tickets=tickets)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['psw']
              
        if(methods.checkUser(username, password)):
            session['user'] = username
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
    if "user" in session:
        user = session['user']
        return render_template('mainmenu.html', username = user)
    else:
        return redirect(url_for('login'))
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)