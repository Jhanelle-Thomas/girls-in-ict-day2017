from . import db
from datetime import datetime

"""class Location(db.Model):
    name = db.Column(db.String(255))
    latitude = 
    longitude = 
    num = 
"""
class SystemUser(db.Model):
    userid = db.Column(db.String(80), primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    email = db.Column(db.String(255))
    password = db.Column(db.String(80))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Message(db.Model):
    messid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    forumid = db.Column(db.Integer)
    title = db.Column(db.String(80))
    message = db.Column(db.String(255))
    author = db.Column(db.String(80))
    time = db.Column(db.DateTime)
    
    def noteTime(self):
        self.time = str(datetime.now())
    
    def getMessage(self):
        return self.message
        
    def getAuthor(self):
        return self.author
        
    def getTime(self):
        return self.time
        
class Forum(db.Model):
    forumid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    forumname = db.Column(db.String(80))
    
    def postToForum(self, message):
        message.forumid = self.forumid
 
class forummessages(db.Model):
    forumid = db.Column(db.Integer, primary_key=True)
    messid = db.Column(db.Integer, primary_key=True)
    
class Project(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    sig = db.Column(db.String(80))
    url = db.Column(db.String(255))
    
    def createTask(self, task):
        task.pid = self.pid

class projectparticipants(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, primary_key=True)

class taskparticipants(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, primary_key=True)

class Task(db.Model):
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer)
    sig = db.Column(db.String(80))
    taskname = db.Column(db.String(80))
    assignee = db.Column(db.String(80))
    description = db.Column(db.String(255))
    progress = db.Column(db.String(80))
    
    def updateProgress(self,up):
        self.progress = up
        
class InterestGroup(db.Model):
    gid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    leader = db.Column(db.String(80))
    leaderid = db.Column(db.String(80))

class Request(db.Model):
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sig = db.Column(db.String(80))
    tid = db.Column(db.Integer)
    tname = db.Column(db.String(80))
    userid = db.Column(db.String(80))
    uname = db.Column(db.String(80))

class Report(db.Model):
    reid = db.Column(db.Integer, primary_key=True, autoincrement=True)