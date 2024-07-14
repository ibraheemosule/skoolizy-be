from sqlalchemy import Enum, String, Time, Date, Integer, TIMESTAMP, func, CheckConstraint, Index
from db import db
from sqlalchemy.orm import validates


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    tag = db.Column(String(30), primary_key=True, unique=True)
    first_name = db.Column(String(50), nullable=False)
    last_name = db.Column(String(50), nullable=False)
    other_name = db.Column(String(50), nullable=True)
    gender = db.Column(Enum('male', 'female', name='gender_enum'), nullable=False)
    date_of_birth = db.Column(Date, nullable=False)
    country = db.Column(String(50), nullable=False)
    state_of_origin = db.Column(String(50), nullable=False)
    email = db.Column(String(50), nullable=False)
    tier = db.Column(Enum("1", '2', '3', '4', '5'), default='1')
    role = db.Column(Enum('staff'), default='staff')

    __table_args__ = (Index('idx_name', tag),)

    def get_id(self):
        return self.id

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "other_name": self.other_name,
            'gender': self.gender,
            "date_of_birth": self.date_of_birth,
            "country": self.country,
            "state_of_origin": self.state_of_origin,
            'email': self.email,
            "tier": self.tier,
            "role": self.role,
            "tag": self.tag,
        }

    @validates('first_name', 'last_name', 'other_name', 'country', 'state_of_origin', 'email')
    def validate_title(self, key, value):
        if not value:
            return value
        if len(value.strip()) < 3 or len(value.strip()) > 50:
            raise ValueError(f"{key} must be a minimum of 10 and maximum of 50 characters")
        return value.strip()
