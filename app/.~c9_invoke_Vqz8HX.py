from . import db
from datetime import datetime

class SytemUser(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
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
    messid = db.Column(db.Integer, primary_key=True)
    forumid = db.Column(db.Integer)
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
    forumid = db.Column(db.Integer, primary_key=True)
    forumname = db.Column(db.String(80))
    
class Project(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    sig = db.Column(db.String(80))

class Task(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    name = db.Column(db.String(80))
    
    description = db.Column(db.String(255))
    progress = db.Column(db.Integer)
    def updateProgress(progress)
    def updateProgress(up):
        self.progress = up