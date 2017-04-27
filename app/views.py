from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, jsonify, make_response, session, flash
from flask_login import login_user, logout_user, current_user, login_required
import requests
from .forms import *
from .models import *
import time
from werkzeug.utils import secure_filename
import os

class DBController:
        
    def postToDatabase(self, obj):
        db.session.add(obj)
        db.session.commit()
        
    def readFromDataabase(self, obj, stat):
        if stat == 'first':
            return obj.first()
        elif stat == 'all':
            return obj.query.all()
            
    def deleteFromDatabase(self, obj):
        db.session.delete(obj)
        db.session.commit()
    
dbcontroller = DBController()

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route("/message", methods=["GET", "POST"])
def forum():
    form = MessageForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            message = form.message.data
            author = session['name']
            mtime = time.strftime('%c')
            
            mObj = Message(forumid=1,title=title,message=message,author=author)
            mObj.noteTime()
            
            dbcontroller.postToDatabase(mObj)
            
    messages = dbcontroller.readFromDataabase(Message(), 'all')
            
    return render_template("forum.html",form=form, messages = messages)
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    form = SignUpForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            userid = genId(first_name, last_name)
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = SystemUser(userid=userid, first_name=first_name, last_name=last_name, username=username,email = email,password=password)
            dbcontroller.postToDatabase(user)
            flash('You were registered')
            return redirect(url_for('login'))
            
    return render_template("signup.html",form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            userObj = SystemUser.query.filter_by(username=username, password=password)
            user = dbcontroller.readFromDataabase(userObj, 'first')
            
            if user is not None:
                session['logged_in'] = True
                session['name'] = user.first_name + " " + user.last_name
                session['userid'] = user.userid
                flash('You were logged in')
                return redirect(url_for('home'))
                
    return render_template('login.html', form=form)
  
@app.route("/app")  
def application ():
    return render_template('InteractiveApp.html')
    
@app.route("/blog")
def blog():
    return render_template('blog.html')
    
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    
@app.route('/addTrash', methods=['POST', 'GET'])
def addTrash():
    file_folder = app.config["UPLOAD_FOLDER"]

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(file_folder, filename))

        flash('Trash Item Added')
        return redirect(url_for('addTrash'))

    return render_template('addtrash.html')
    
@app.route('/logout')
#@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))
    
@login_manager.user_loader
def load_user(id):
    return SystemUser.query.get(int(id))

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

def genId(fname, lname):
    nid = []
    for x in fname:
        nid.append(str(ord(x)))
    for x in lname:
        nid.append(str(ord(x)))
    random.shuffle(nid)
    nid = "".join(nid)
    return nid[:7]

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
