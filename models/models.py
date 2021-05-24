import sys
sys.path.append('..\\modules\\')

# from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

from config.config import SetDatabase

# Create an instance of SetDatabase class with json configuration
database_config = SetDatabase('..\\config.json')

db_string = database_config.connection_string

db = SQLAlchemy()

''' 
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=db_string):

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Vessel(db.Model):
    """
    Class used to map vessels into database.
    """
    __tablename__ = 'vessels'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(), nullable=False, unique=True)

    # one-to-many relationship definition between vessels and equipments.
    equipments = db.relationship('Equipment', backref='vessels', lazy=True)
    

    def __init__(self, code):

        self.code = code

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id, 
            'code': self.code
        }

class Equipment(db.Model):
    """
    Class used to map equipments into database.
    """
    __tablename__ = 'equipments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    code = db.Column(db.String(), nullable=False, unique=True)
    location = db.Column(db.String(), nullable=False)
    activation_status = db.Column(db.Boolean, default=True, nullable=False)

    # Defintion of the foreign key to link equipments with vessels.
    vessel_code = db.Column(db.String(), db.ForeignKey('vessels.code'), nullable=False)

    def __init__(self, name, code, location, vessel_code=True):

        self.name = name
        self.code = code
        self.location = location
        self.vessel_code = vessel_code

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id, 
            'name': self.name,
            'code': self.code,
            'location': self.location,
            'activation_status': self.activation_status,
            'vessel_code': self.vessel_code 
        }