from sqlalchemy import TIMESTAMP, Enum, String, Date, Integer, Boolean, func, orm
from configs.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from utils.error_handlers import CustomError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, pre_load, validate, validates_schema

from utils.helpers import get_date_and_time, has_special_char, is_password_valid, years_diff


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(Integer, unique=True, autoincrement=True, primary_key=True)
    tag = db.Column(String(30), nullable=False, unique=True)
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
    created_at = db.Column(TIMESTAMP(timezone=True), default=func.current_timestamp())
    password = db.Column(String(255))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id

    @orm.validates('password')
    def validate_and_hash_password(self, key, value):
        if value:
            return generate_password_hash(value)
        return value


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True

    tag = fields.String(required=True)
    first_name = fields.String(required=True, validate=[validate.Length(min=2, max=40)])
    middle_name = fields.String(validate=validate.Length(min=2, max=40), allow_none=True, missing=None)
    last_name = fields.String(required=True, validate=[validate.Length(min=2, max=40)])
    gender = fields.String(validate=validate.OneOf(['male', 'female']), required=True)
    date_of_birth = fields.Date(required=True)
    country = fields.Str(validate=validate.Length(min=3, max=50), required=True)
    state_of_origin = fields.Str(validate=validate.Length(min=2, max=50), required=True)
    phone_number = fields.Str(validate=validate.Length(min=8, max=15), required=True)
    home_address = fields.Str(validate=validate.Length(min=2, max=100), required=True)
    email = fields.String(validate=validate.Email(), required=True, unique=True)
    tier = fields.Int(validate=validate.OneOf([1, 2, 3, 4, 5]))
    role = fields.Str(validate=validate.OneOf(['staff']), required=True)
    verified = fields.Bool()
    created_at = fields.DateTime()
    password = fields.Str(load_only=True, required=True)

    @pre_load
    def format_date_of_birth(self, data, **kwargs):
        if dob := data.get('date_of_birth'):
            try:
                data["date_of_birth"] = get_date_and_time(dob)["date"]
            except ValueError:
                raise CustomError('Invalid date of birth provided')

        return data

    @validates_schema
    def validating_staff(self, data, **kwargs):
        if has_special_char(data.get('first_name')):
            raise CustomError("first_name contains invalid characters")

        if has_special_char(data.get('middle_name')):
            raise CustomError("middle_name contains invalid characters")

        if has_special_char(data.get('last_name')):
            raise CustomError("last_name contains invalid characters")

        if not is_password_valid(password=data.get('password')):
            raise CustomError(
                'Password must be a minimum of 8 characters long and must contain a capital letter, a small letter, a number and a symbol'
            )

        if years_diff(data.get("date_of_birth")) < 18:
            raise CustomError("Date of birth should be at least 18 years ago")
