# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 10:40:09 2018

@author: Ayush
"""
from dynamo import getpass, setdets, query
from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "POST":		
        attempted_username = request.form['username']
        if query(attempted_username) == False:
            k=getpass(attempted_username)
            if sha256_crypt.verify(request.form['password'],k):
               session['logged_in'] = True
               session['username'] = request.form['username']
               flash("You are now logged in")
               return render_template("welcome.html", uname = attempted_username)
            else:
                flash("Invalid credentials, try again.")
                return render_template("index.html")
        else:
            flash('No such user detected please signup!')
            return redirect(url_for('register_page'))
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
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            if query(username) == True:
                setdets(username,password,email)
                session['logged_in'] = True
                session['username'] = username
                return render_template("welcome.html", uname = username)
            else:
                flash('Username taken')
                return render_template("register.html", form=form)
        return render_template("register.html", form=form)

#using wrappers
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('home'))
    return wrap

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True,port=6969)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'