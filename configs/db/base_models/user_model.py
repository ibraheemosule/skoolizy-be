from typing import Dict
from sqlalchemy import TIMESTAMP, String, Boolean, func, Enum, Date, Integer
from configs.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from utils.error_handlers import CustomError
from sqlalchemy import orm


class UserModel(db.Model):
    __abstract__ = True

    id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tag = db.Column(String(30), nullable=False, unique=True)
    created_at = db.Column(TIMESTAMP(timezone=True), default=func.current_timestamp())
    first_name = db.Column(String(50), nullable=False)
    middle_name = db.Column(String(50), nullable=True)
    last_name = db.Column(String(50), nullable=False)
    gender = db.Column(Enum('male', 'female', name='gender_enum'), nullable=False)
    date_of_birth = db.Column(Date, nullable=False)
    country = db.Column(String(50), nullable=False)
    phone_number = db.Column(String(15), nullable=False)
    home_address = db.Column(String(200), nullable=False)
    state_of_origin = db.Column(String(50), nullable=False)
    email = db.Column(String(50), nullable=False, unique=True)
    tier = db.Column(Integer, default=1)
    role = db.Column(String(20), default='staff')
    verified = db.Column(Boolean, default=False)
    password = db.Column(String(255))

    @classmethod
    def get_by_tag(cls, tag: str):
        """Fetch a record by its unique tag."""
        return cls.query.filter_by(tag=tag).first()

    @classmethod
    def update(cls, model: Dict, tag: str):
        """Update fields of a record identified by its tag."""
        instance = cls.get_by_tag(tag)
        if not instance:
            raise CustomError(f"Record with tag '{tag}' not found.")
        for key, value in model.items():
            if value and hasattr(instance, key):
                setattr(instance, key, value)

        db.session.commit()
        return instance

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password, password)

    def get_tag(self):
        """Get the unique tag of the user."""
        return self.tag

    @orm.validates('password')
    def validate_and_hash_password(self, key, value):
        """Validate and hash the password."""
        if value:
            return generate_password_hash(value)
        return value

    @orm.validates('country', 'verified', 'created_at', 'state_of_origin', 'gender', 'date_of_birth')
    def set_once(self, key, value):
        """Ensure certain fields are set only once."""
        if getattr(self, key) is not None:
            raise CustomError(f"{key} cannot be updated once set.")
        return value
