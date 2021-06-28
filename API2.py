"""
Local Database has been implemented and the table creation command has been commented (In create method).
Local SQLite Database can be initialized by changing the directory.

"""

import os
import sqlite3

from flask import Flask, request, jsonify, render_template
os.chdir("/mnt/d/programs/FlaskAPI/API1")
app = Flask(__name__)

# Homepage rendering

@app.route('/',methods = ["GET"])
def hello():
    return render_template('base.html')

# User creation

@app.route('/create',methods = ["GET","POST"])
def addUser():
    if request.method == "POST":
        conn = sqlite3.connect('Data2.db')
        cursor = conn.cursor()
        #cursor.execute("CREATE TABLE content (name TEXT NOT NULL UNIQUE, description JSON);")
        uname = request.form['username']
        try:
            cursor.execute("INSERT INTO content (username, name, dob, age, edu) VALUES (?,?,?,?,?)",(uname,'', '', 0, ''))
            conn.commit()
        except:
            return render_template("create.html", msg = {"Message":"Username Already Exists!"})
        return render_template("update.html",flag=True,uname=uname,msg={"Message":"User Created Successfully!"})
    else:
        return render_template("create.html")

# Data Updation

@app.route('/update',methods = ["GET","POST"])
def update():
    if request.method == "POST":
        name = request.form['username']
        conn = sqlite3.connect('Data2.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM content where username = (?)",(name,))
        if cursor.fetchone() is not None:
            try:
                n = request.form['name']
                dob = request.form['dob']
                age = int(request.form['age'])
                edu = request.form['edu'] 
                cursor.execute("UPDATE content SET name = ?, dob = ?, age = ?, edu = ? WHERE username = ? ",(n,dob,age,edu,name))
                conn.commit()
                return render_template("base.html",js={"Message":"Saved"})
            except:
                return render_template("update.html",flag=True,uname=name)    
        else:
            return render_template("base.html",js={"Message":"User not found!"})
            
    if request.method == "GET":
        return render_template("update.html")

# Reading the data

@app.route('/retrieve',methods = ["GET","POST"])
def show():
    if request.method == "POST":
        uname = request.form['username']
        conn = sqlite3.connect('Data2.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM content where username = (?)",(uname,))
        try:
            data = cursor.fetchone()
            re = {
                "name" : data[1],
                "dob" : data[2],
                "age" : data[3],
                "edu" : data[4]
            }
            return render_template("view.html",flag=True,re=re)
        except:
            return render_template("base.html",js={"Message":"User not found!"})
    else:
        return render_template("view.html")

# User Deletion

@app.route('/remove',methods = ["GET","POST"])
def remove():
    if request.method == "GET":
        return render_template("delete.html")
    uname = request.form['username']
    conn = sqlite3.connect('Data2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM content where username = (?)",(uname,))
    if cursor.fetchone() is not None:
        cursor.execute("DELETE FROM content WHERE username = (?)",(uname,))
        conn.commit()
        return render_template("base.html",js={"Message":"User Deleted!"})
    else:
        return render_template("base.html",js={"Message":"User not found!"})


if __name__ == "__main__":
    app.run(debug=True)