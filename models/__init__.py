from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from models import detections
from models import patients
from models import users
import app