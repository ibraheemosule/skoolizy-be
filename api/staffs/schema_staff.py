from marshmallow import fields, validate, validates
from api.staffs.model_staffs import Staff
from configs.db.base_schemas.user_schema import UserSchema
from utils.error_handlers import CustomError
from utils.helpers import years_diff
from utils.constants import user_titles


class StaffSchema(UserSchema):
    class Meta:
        model = Staff
        load_instance = True

    # Staff specific schema
    title = fields.Str(validate=validate.OneOf([*user_titles]), required=True)

    @validates("date_of_birth")
    def validate_dob(self, dob: str):
        if years_diff(dob) < 16:
            raise CustomError("Date of birth should be at least 16 years ago")
