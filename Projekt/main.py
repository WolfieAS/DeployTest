from flask import Flask
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

# creates an application that is named after the name of the file
app = Flask(__name__)

@app.route('/')
def index():
   return "Hello World"


@app.route('/login', methods=['GET', 'POST'])
def login():
   return render_template('login.html')

  
if __name__ == "__main__":
    app.run(debug=True)
