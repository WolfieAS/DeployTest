import uuid

import psycopg2
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from DBOperations import DBQueries as db
from fileinput import filename
from flask_cors import CORS
from flask_apscheduler import APScheduler

app = Flask(__name__, static_folder="Photos")
CORS(app)
app.secret_key="hello"


@app.route('/')
def index():
    tickets = db.getAllTickets()
    if "user" in session:
        user = session['user']
        return render_template('index.html', tickets=tickets, username=user)
    else:
        return render_template('index.html', tickets=tickets)


@app.route('/allTickets', methods=['GET'])
def allTickets():
    t = db.getAllTickets()
    result = []
    for i in range(len(t)):
        obj = db.Ticket(t[i][0], t[i][1], t[i][2], t[i][3], t[i][4], t[i][5], t[i][6], t[i][7], t[i][8])
        result.append(obj.__dict__)
        print(t[i]) 
    return jsonify(result), 200
    

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['psw']
        val, user = db.checkUser(username, password)
        if val:
            session['user'] = user.email
            session['user_id'] = user.id
            session['usertype'] = user.usertype
            session['responsible'] = user.responsible_for
            return redirect(url_for('mainmenu'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')
"""


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    val, user = db.checkUser(email, password)
    if val:
        return user.__dict__, 200
    else:
        return "",403


@app.route('/checkticket', methods=['GET'])
def check():
    ticket_id = request.args.get("ticketid")
    serial_no = request.args.get("serialno")
    location = request.args.get("location")
    return jsonify(db.checkTicket(ticket_id, serial_no, location))  , 200


@app.route('/banticket', methods=['GET'])
def ban():
    serial_no = request.args.get("serialno")
    return jsonify(db.updateTicketActive(serial_no, False, "test")) , 200


@app.route('/unbanticket', methods=['GET'])
def unban():
    serial_no = request.args.get("serialno")
    return jsonify(db.updateTicketActive(serial_no, True, "")) , 200


'''@app.route('/register', methods=['GET', 'POST'])
def register():   
    if request.method == "POST":
        username = request.form['uname']
        email = request.form['email']
        password = request.form['psw']
        #Validity check
        password = db.hashPassword(password) # Hash password
        db.addUser(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')'''


@app.route('/register', methods=['POST'])
def register():   
    data = request.get_json()
    email = data['email']
    password = data['password']
    firstName = data['firstName']
    lastName = data['lastName']
    agb = data['agb']
    birthday = data['birthday']
    phonenumber = data['phonenumber']
    #Validity check
    password = db.hashPassword(password) # Hash password
    try:
        db.addUser(email, password, firstName, lastName, agb, birthday, phonenumber)
        return "",200
    except psycopg2.errors.UniqueViolation:
        return "",409


@app.route('/mainmenu', methods=['GET', 'POST'])
def mainmenu():
    if "user" in session:
        user = session['user']
        return render_template('mainmenu.html', username = user)
    else:
        return redirect(url_for('login'))


@app.route('/mytickets', methods=['POST'])
def myTickets():
    data = request.get_json()
    user_id = data['userid']
    t = db.getAllActiveTicketsFromUser(user_id)

    result = []
    for i in range(len(t)):
        obj = db.RegTicket(t[i][0], t[i][1], t[i][2], t[i][3], t[i][4], t[i][5], t[i][6], t[i][7], t[i][8], t[i][9], t[i][10], t[i][11], t[i][12], t[i][13])
        result.append(obj.__dict__)
    if bool(t):
        return jsonify(result), 200
    else:
        return '', 200


@app.route('/proveTicket', methods=['POST'])
def proveTicket():
    data = request.get_json()
    serial_no = data['serialno']   
    t = db.getRegTicket(serial_no)
    result = []
    for i in range(len(t)):
        obj = db.RegTicket(t[i][0], t[i][1], t[i][2], t[i][3], t[i][4], t[i][5], t[i][6], t[i][7], t[i][8], t[i][9], t[i][10], t[i][11], t[i][12],t[i][13])
        result.append(obj.__dict__)
    if bool(t):
        return jsonify(result), 200
    else:
        return 'serialno no found', 400
    
        

    

@app.route('/mytickets/<serial_no>', methods=['GET', 'POST'])
def qrcode(serial_no):
    
    if db.checkSerial_no(serial_no):
        db.createQRCode(serial_no)
    
    return redirect(url_for('myTickets'))


@app.route('/prove/<serial_no>', methods=['GET', 'POST'])
def proveQR(serial_no):
    serial_no = str(serial_no)
    usertype = session['usertype']
    responsible = session['responsible']
    if int(usertype)==2:
        if db.checkSerial_no(serial_no):
            db.redeem_ticket(serial_no, responsible)
            info = db.checkTicketOld(serial_no)
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
        if db.checkUser(username, oldpassword):
            db.updatePasswort(username, db.hashPassword(newpassword))
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('index'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))


@app.route('/buy', methods=['POST'])
def buy():
    data = request.get_json()
    ticket_id = data.get("ticketid", 1)
    print(db.getTicket(ticket_id))
    ticket = db.ticketFromDB(db.getTicket(ticket_id)[0])
    db.registrateTicket(uuid.uuid4().hex, data.get("userid",0), ticket_id, data.get("vorname"), data.get("Nachname"), data.get("Geburtsdatum"), ticket.valid_from, ticket.valid_to, 5, data.get("Tarif"), data.get("Handynummer"), data.get("E-Mail-Adresse"))
    return "" , 200


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

def deleteDataAfter30Days():
    deleteDate = db.getDateMinus30Days()
    db.deleteOldRedeemedTickets(deleteDate)
    
if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.add_job(func=deleteDataAfter30Days, trigger='interval', id='job', days=30) #days sollte auf 1 gestellt werden, damit der job taeglich laeuft
    scheduler.start()
    app.run(debug=True)
