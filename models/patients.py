from datetime import date, datetime
from models import db
from sqlalchemy.orm import relationship

class Patients(db.Model):
    __tablename__ = 'patients'
    __table_args__ = {'extend_existing': True}


    id = db.Column(db.String(8), unique = True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    nik = db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.String(3))
    date_of_birth = db.Column(db.String(30))
    address = db.Column(db.String(150))

    children = relationship("Detection")

class Detection(db.Model):
    __tablename__ = 'detections'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(8), unique = True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)
    patient_id = db.Column(db.String(8), db.ForeignKey('patients.id'), nullable=False)
    file_path = db.Column(db.String(160), nullable=False)



