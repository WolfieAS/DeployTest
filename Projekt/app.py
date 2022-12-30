from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
import psycopg2
import bcrypt
from DBOperations import DBQueries as db
from DBOperations import methods
from DBOperations.methods import checkSerial_no
from fileinput import filename


app = Flask(__name__, static_folder="Photos")
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
            session['usertype']=methods.getUsertype(username)
            session['responsible']=methods.getResponsible_for(username)
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
        redeemed_tickets = db.getUser_redeemed_tickets(user_id)
        ticket = methods.groupTickets(ticket, redeemed_tickets)
        if bool(ticket):
            return render_template('tickets.html', username = user, ticket=ticket, qrcode = filename)
        else:
            return render_template('tickets.html', username = user, message = "Du hast keine Tickets") 
        
    else:
        return redirect(url_for('login'))
    
@app.route('/mytickets/<serial_no>', methods=['GET', 'POST'])
def qrcode(serial_no):
    
    if checkSerial_no(serial_no):
        methods.createQRCode(serial_no)
    
    return redirect(url_for('myTickets'))

@app.route('/prove/<serial_no>', methods=['GET', 'POST'])
def proveQR(serial_no):
    serial_no = str(serial_no)
    usertype = session['usertype']
    responsible = session['responsible']
    if int(usertype)==2:
        if methods.checkSerial_no(serial_no):
            db.reedem_ticket(serial_no, responsible)
            info = db.checkTicket(serial_no)
            return render_template('prove.html', info = info)
        else:
            return render_template('prove.html', message = "Ticket existiert nicht")
    else:
        return redirect(url_for('index'))
    
@app.route('/profile/restartpassword', methods=['GET', 'POST'])
def restartpassword():
    if "user" in session:
        username = session['user']
        oldpassword = "test"
        newpassword = "test1"
        if(methods.checkUser(username, oldpassword)):
            db.updatePasswort(username, methods.hashPassword(newpassword))
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('index'))
       
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
