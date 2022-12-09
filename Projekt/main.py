from flask import Flask
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

# creates an application that is named after the name of the file
app = Flask(__name__)

@app.route('/')
def index():
   return "Hello World"
  
if __name__ == "__main__":
    app.run()
