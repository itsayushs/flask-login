# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 10:40:09 2018

@author: Ayush
"""
from dynamo import getpass, setdets, query
from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "POST":		
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        user="ayush"
        if attempted_username == "admin" and attempted_password == "password":
            return render_template("welcome.html", uname = user)				
        else:
            return render_template("logout.html")
    else:
        return render_template("index.html")

#createing the form in flask
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
@app.route('/register/', methods=["GET","POST"])
def register_page():
        app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            setdets(username,password,email)
            session['logged_in'] = True
            session['username'] = username
        return render_template("register.html", form=form)
        
if __name__ == "__main__":
    app.run(debug=True,port=6969)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'