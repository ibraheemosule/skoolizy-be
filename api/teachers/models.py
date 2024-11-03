from sqlalchemy import Enum, String, Date, Integer, Index, Boolean
from configs.db import db
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash
from utils.error_handlers import CustomError


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(Integer, unique=True, autoincrement=True, primary_key=True)
    tag = db.Column(String(30), nullable=False, unique=True)
    first_name = db.Column(String(50), nullable=False)
    last_name = db.Column(String(50), nullable=False)
    middle_name = db.Column(String(50), nullable=True)
    gender = db.Column(Enum('male', 'female', name='gender_enum'), nullable=False)
    date_of_birth = db.Column(Date, nullable=False)
    country = db.Column(String(50), nullable=False)
    phone_number = db.Column(String(15), nullable=False)
    home_address = db.Column(String(200), nullable=False)
    state_of_origin = db.Column(String(50), nullable=False)
    email = db.Column(String(50), nullable=False, unique=True)
    tier = db.Column(Enum("1", '2', '3', '4', '5'), default='1')
    role = db.Column(Enum('staff'), default='staff')
    verified = db.Column(Boolean, default=False)
    password_hash = db.Column(String(255), nullable=False)

    __table_args__ = (Index('idx_name', tag),)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_id(self):
        return self.id

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            'gender': self.gender,
            "date_of_birth": self.date_of_birth,
            "country": self.country,
            "state_of_origin": self.state_of_origin,
            'phone_number': self.phone_number,
            "hone_address": self.home_address,
            'email': self.email,
            "tier": self.tier,
            "role": self.role,
            "tag": self.tag,
            "verified": self.verified,
        }

    @validates(
        'first_name', 'last_name', 'middle_name', 'country', 'state_of_origin', 'email', 'phone_number', 'home_address'
    )
    def validate_title(self, key, value):
        if not value or not isinstance(value, str):
            raise CustomError(f"{key} has an invalid value", 403)

        val_len = len(value.strip())

        if key == 'home_address':
            if val_len < 20 or val_len > 200:
                raise CustomError(f"{key} must be a minimum of 20 characters and maximum of 200 characters", 403)
            return value.strip()

        if val_len < 3 or val_len > 50:
            raise CustomError(f"{key} must be a minimum of 10 and maximum of 50 characters", 403)
        return value.strip()

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)
