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
    detection = db.Column(db.String(160))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_patient_id(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def single_patient_histories(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id).all()

    @classmethod
    def latest_all(cls):
        subq = db.session.query(Detection.patient_id, func.max(Detection.created_at).label("created_at")).group_by(Detection.patient_id).subquery('t1')
        # detection_query = db.session.query(Detection).join(subq, and_ (
        #     Detection.patient_id == subq.c.patient_id,
        #     Detection.created_at == subq.c.created_at
        # )).subquery('t2')
        # return db.session.query(Patients, detection_query).join(detection_query, and_(
        #     Patients.id == detection_query.c.patient_id,
        # ), full=True).all()
        return db.session.query(Patients.name, Patients.patient_number, Patients.age, Patients.address, Detection.patient_id, Detection.created_at, Detection.detection, Detection.file_path).select_from(Patients).join(Detection, full=True).join(subq, and_(
            Patients.id == subq.c.patient_id,
            Detection.patient_id == subq.c.patient_id,
            Detection.created_at == subq.c.created_at
        )).all()


