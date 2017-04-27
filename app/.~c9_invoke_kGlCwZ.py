from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, jsonify, make_response, session, flash
from flask_login import login_user, logout_user, current_user, login_required
import requests
from .forms import *
from .models import *
import time

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
    
@app.route("/createProject", methods=["GET","POST"])
def createproject():
    
    form = ProjectForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            desc = form.description.data
            sig = form.sig.data
            url = form.url.data
            
            proj = Project(name=name, description=desc, sig=sig, url=url)
            
            dbcontroller.postToDatabase(proj)
            return redirect(url_for('viewproj'))
            
    return render_template("createproject.html",form=form)
    
@app.route("/createTask", methods=["GET","POST"])
def createtask():
    
    form = TaskForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.assignee.data
            desc = form.description.data
            project = form.projectname.data
            tname = form.taskname.data
            
            pObj = Project.query.filter_by(name=project)
            proj = dbcontroller.readFromDataabase(pObj, 'first')
            
            task = Task(pid=proj.pid, assignee=name, description=desc, progress=0, sig=proj.sig, taskname=tname)
            
            dbcontroller.postToDatabase(task)
            return redirect(url_for('viewtasks'))
            
    return render_template("createtask.html",form=form)
    
@app.route("/requests", methods=["POST"])
def requestsT():
    if request.method == "POST":
        form = RequestForm()
        
        if form.validate_on_submit():
            sig = form.sig.data
            tid = form.tid.data
            taskname = form.taskname.data
            uname = form.uname.data
            uid = session['userid']
            
            req = Request(tid=tid,sig=sig,tname=taskname,uname=uname,userid=uid)
            
            dbcontroller.postToDatabase(req)
            
            flash('You request has been submitted')
            return redirect(url_for('home'))
            
@app.route('/viewrequests', methods=["GET"])
def viewrequests():
    requests = dbcontroller.readFromDataabase(Request(), 'all')
    return render_template("viewrequests.html", requests=requests)

@app.route("/viewProjects", methods=["GET"])
def viewproj():
    projects = dbcontroller.readFromDataabase(Project(), 'all')
    return render_template("viewprojects.html", projects=projects)

@app.route("/viewTasks", methods=["GET"])
def viewtasks():
    tasks = dbcontroller.readFromDataabase(Task(), 'all')
    return render_template("viewtasks.html",tasks=tasks, form=RequestForm())
    
@app.route('/accept/<int:rid>',methods=["POST"])
def accept(rid):
@app.r
    if request.method == "POST":
        req = dbcontroller.readFromDataabase(Request.query.filter_by(rid=rid), 'first')
    
        t = taskparticipants(userid=req.userid, tid=req.tid)
        
        task = dbcontroller.readFromDataabase(Task.query.filter_by(tid=t.tid), 'first')
        proj = dbcontroller.readFromDataabase(Project.query.filter_by(pid=task.pid), 'first')
        
        p = projectparticipants(userid=req.userid, pid=proj.pid)
        
        dbcontroller.postToDatabase(t)
        dbcontroller.postToDatabase(p)
        
        dbcontroller.deleteFromDatabase(req)
    
        flash('Request Accepted')
        return redirect(url_for('home'))

@app.route('/reject/<int:rid>',methods=["POST"])
def reject(rid):
    
    if request.method == "POST":
        req = dbcontroller.readFromDataabase(Request.query.filter_by(rid=rid), 'first')
        dbcontroller.deleteFromDatabase(req)
        flash('Request Rejected')
        return redirect(url_for('home'))

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
            userid = form.id_num.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            password = form.password.data
            sig = form.special_interest_group.data
            acctype = form.acctype.data
            
            user = SystemUser(userid=userid, first_name=first_name, last_name=last_name, username=username,
            password=password, sig=sig, acctype=acctype)
            
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
                session['account_type'] = user.acctype ## store account type to handle MVC stuff
                session['sig'] = user.sig
                session['name'] = user.first_name + " " + user.last_name
                session['userid'] = user.userid
                flash('You were logged in')
                return redirect(url_for('home'))
                
    return render_template('login.html', form=form)
    
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


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
