from utils.error_handlers import CustomError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, pre_load, validate, validates_schema
from utils.helpers import get_date_and_time, has_special_char, is_password_valid, years_diff


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        exclude = (id,)
        load_instance = True

    tag = fields.String(dump_only=True)
    first_name = fields.String(required=True, validate=[validate.Length(min=2, max=40)])
    middle_name = fields.String(validate=validate.Length(min=2, max=40), allow_none=True, missing=None)
    last_name = fields.String(required=True, validate=[validate.Length(min=2, max=40)])
    gender = fields.String(validate=validate.OneOf(['male', 'female']), required=True)
    date_of_birth = fields.Date(required=True)
    country = fields.Str(validate=validate.Length(min=3, max=50), required=True)
    state_of_origin = fields.Str(validate=validate.Length(min=2, max=50), required=True)
    phone_number = fields.Str(validate=validate.Length(min=8, max=15), required=True)
    home_address = fields.Str(validate=validate.Length(min=2, max=100), required=True)
    email = fields.String(validate=validate.Email(), required=True)
    tier = fields.Int(validate=validate.OneOf([1, 2, 3, 4, 5]))
    role = fields.Str(validate=validate.OneOf(['staff']), required=True)
    verified = fields.Bool()
    created_at = fields.DateTime()
    password = fields.Str(load_only=True, required=True)

    @pre_load
    def format_date_of_birth(self, data, **kwargs):
        """Format the date_of_birth field before loading the data"""
        if dob := data.get('date_of_birth'):
            try:
                data["date_of_birth"] = get_date_and_time(dob)["date"]
            except ValueError:
                raise CustomError('Invalid date of birth provided')
        return data

    @validates_schema
    def validate_schema(self, data, **kwargs):
        """Custom validation logic for the schema"""

        if has_special_char(data.get('first_name')):
            raise CustomError("first_name contains invalid characters")

        if has_special_char(data.get('middle_name')):
            raise CustomError("middle_name contains invalid characters")

        if has_special_char(data.get('last_name')):
            raise CustomError("last_name contains invalid characters")

        password = data.get('password')
        if password and not is_password_valid(password=password):
            raise CustomError(
                'Password must be a minimum of 8 characters long and must contain a capital letter, a small letter, a number and a symbol'
            )

        if years_diff(data.get("date_of_birth")) < 18:
            raise CustomError("Date of birth should be at least 18 years ago")
