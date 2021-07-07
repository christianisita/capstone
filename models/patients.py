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
    patient_number = db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.String(3))
    date_of_birth = db.Column(db.String(30))
    address = db.Column(db.String(150))

    children = relationship("Detection")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_patient_number(cls, patient_number):
        return cls.query.filter_by(patient_number = patient_number).first()
    
    @classmethod
    def find_by_patient_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_patient_data(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_patient_name(cls, id):
        return cls.query.filter_by

class Detection(db.Model):
    __tablename__ = 'detections'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(8), unique = True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)
    patient_id = db.Column(db.String(8), db.ForeignKey('patients.id'), nullable=False)
    file_path = db.Column(db.String(160), nullable=False)



