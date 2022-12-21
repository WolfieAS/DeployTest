from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
import psycopg2
import bcrypt
from DBOperations import DBQueries as db
from helperMethods import methods
from helperMethods.methods import checkSerial_no


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
            session['user_id'] = methods.getUser_id(username)
            return redirect(url_for('mainmenu'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

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
    
@app.route('/mytickets', methods=['GET', 'POST'])
def myTickets():
    if "user" in session:
        user = session['user']
        user_id = session['user_id']
        ticket = db.getAllTicketsFromUser(user_id)
        if bool(ticket):
            return render_template('tickets.html', username = user, ticket=ticket)
        else:
            return render_template('tickets.html', username = user, message = "Du hast keine Tickets") 
        
    else:
        return redirect(url_for('login'))
    
@app.route('/mytickets/<serial_no>', methods=['GET', 'POST'])
def qrcode(serial_no):
    
    if checkSerial_no(serial_no):
        methods.createQRCode(serial_no)
    
    return redirect(url_for('myTickets'))
   
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)