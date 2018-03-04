# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 10:40:09 2018

@author: Ayush
"""
from flask import Flask,render_template,redirect,request,url_for

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "POST":		
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        user="ayush"
        if attempted_username == "admin" and attempted_password == "password":
            return render_template("su.html", uname = user)				
        else:
            return render_template("usu.html")
    else:
        return render_template("index.html")

@app.route('/su/')
def suc():
    return render_template("su.html")
    
if __name__ == "__main__":
    app.run()
