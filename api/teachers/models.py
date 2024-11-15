from sqlalchemy import Enum, String, Date, Integer, Index, Boolean
from configs.db import db
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash
from utils.error_handlers import CustomError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, pre_load, validate, validates_schema, post_load

from utils.helpers import get_date_and_time, has_special_char, is_password_valid


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
    tier = db.Column(Integer, default=1)
    role = db.Column(String(20), default='staff')
    verified = db.Column(Boolean, default=False)
    password = db.Column(String())

    __table_args__ = (Index('idx_name', tag),)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_id(self):
        return self.id

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "first_name": self.first_name,
    #         "last_name": self.last_name,
    #         "middle_name": self.middle_name,
    #         'gender': self.gender,
    #         "date_of_birth": self.date_of_birth,
    #         "country": self.country,
    #         "state_of_origin": self.state_of_origin,
    #         'phone_number': self.phone_number,
    #         "hone_address": self.home_address,
    #         'email': self.email,
    #         "tier": self.tier,
    #         "role": self.role,
    #         "tag": self.tag,
    #         "verified": self.verified,
    #     }

    # @validates(
    #     'first_name', 'last_name', 'middle_name', 'country', 'state_of_origin', 'email', 'phone_number', 'home_address'
    # )
    # def validate_title(self, key, value):
    #     if not value or not isinstance(value, str):
    #         raise CustomError(f"{key} has an invalid value", 403)

    #     val_len = len(value.strip())

    #     if key == 'home_address':
    #         if val_len < 20 or val_len > 200:
    #             raise CustomError(f"{key} must be a minimum of 20 characters and maximum of 200 characters", 403)
    #         return value.strip()

    #     if val_len < 3 or val_len > 50:
    #         raise CustomError(f"{key} must be a minimum of 10 and maximum of 50 characters", 403)
    #     return value.strip()

    # def check_password(self, password: str):
    #     return check_password_hash(self.password_hash, password)


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True

    tag = fields.String(required=True)
    first_name = fields.String(required=True, validate=[validate.Length(min=2, max=40)])
    middle_name = fields.String(validate=[validate.Length(min=2, max=40)])
    last_name = fields.String(required=True, validate=[validate.Length(min=2, max=40)])
    gender = fields.String(validate=validate.OneOf(['male', 'female']), required=True)
    date_of_birth = fields.Date(required=True)
    country = fields.String(validate=validate.Length(min=3, max=50), required=True)
    state_of_origin = fields.String(validate=validate.Length(min=2, max=50), required=True)
    phone_number = fields.String(validate=validate.Length(min=8, max=15), required=True)
    home_address = fields.String(validate=validate.Length(min=2, max=100), required=True)
    email = fields.String(validate=validate.Email(), required=True)
    tier = fields.Int(validate=validate.OneOf([1, 2, 3, 4, 5]))
    role = fields.String(validate=validate.OneOf(['staff']), required=True)
    verified = fields.Bool()
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
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        if has_special_char(first_name):
            raise CustomError("first_name contains invalid characters")

        if middle_name := data.get('middle_name') and has_special_char(middle_name):
            raise CustomError("middle_name contains invalid characters")

        if has_special_char(last_name):
            raise CustomError("last_name contains invalid characters")

        if not is_password_valid(password=password):
            raise CustomError(
                'Password must be a minimum of 8 characters long and must contain a capital letter, a small letter, a number and a symbol'
            )
