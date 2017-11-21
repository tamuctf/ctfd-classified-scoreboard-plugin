from sqlalchemy import ForeignKey

from CTFd.models import db

class Classification(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, ForeignKey('teams.id'), primary_key=True)
    classification = db.Column(db.String(128))

    def __init__(self, id, classification):
        self.id = id
        self.classification = classification

def create_db(app):
    app.db.create_all()
