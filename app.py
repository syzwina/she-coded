# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect
import sqlite3 

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# Create database
connect = sqlite3.connect('database.db') 
connect.execute( 'CREATE TABLE IF NOT EXISTS CUSTOMERS (name TEXT, email TEXT, city TEXT, country TEXT, phone TEXT)') 
connect.execute( 'CREATE TABLE IF NOT EXISTS ORDERS (customer_email TEXT, bulb_type TEXT, quantity INT, date datetime default current_timestamp)') 

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

@app.route('/Bulbbnb')
def Bulbbnb():
    return render_template('Bulbbnb.html') 
  
@app.route('/form', methods=['GET', 'POST']) 
def join(): 
    if request.method == 'POST': 
        name = request.form['name'] 
        email = request.form['email'] 
        city = request.form['city'] 
        country = request.form['country'] 
        phone = request.form['phone'] 
  
        with sqlite3.connect("database.db") as users: 
            cursor = users.cursor() 
            cursor.execute("INSERT INTO CUSTOMERS (name,email,city,country,phone) VALUES (?,?,?,?,?)", (name, email, city, country, phone)) 
            users.commit() 
        return redirect("/list")
    else: 
        return render_template('form.html') 
  
@app.route('/list') 
def list(): 
    connect = sqlite3.connect('database.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM CUSTOMERS') 
  
    data = cursor.fetchall() 
    return render_template("list.html", data=data) 

@app.route('/order', methods=['GET', 'POST']) 
def order(): 
    if request.method == 'POST': 
        email = request.form['email'] 
        bulb_type = request.form['bulb_type'] 
        quantity = request.form['quantity'] 
  
        with sqlite3.connect("database.db") as users: 
            cursor = users.cursor() 
            cursor.execute("INSERT INTO ORDERS (customer_email,bulb_type,quantity) VALUES (?,?,?)", (email, bulb_type, quantity)) 
            users.commit() 
        return redirect("/orders")
    else: 
        return render_template('order.html') 

@app.route('/orders') 
def orders_list(): 
    connect = sqlite3.connect('database.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM ORDERS') 
  
    data = cursor.fetchall() 
    return render_template("orders_list.html", data=data) 

@app.route('/Bulbbnb/<bulb_name>')
def bulb(bulb_name):
    return render_template('product.html', name=bulb_name, image='/static/bulb1.jpg') 

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()