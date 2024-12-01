from marshmallow import fields, validate, validates
from api.guardians.model_guardians import Guardian
from configs.db.base_schemas.user_schema import UserSchema
from utils.error_handlers import CustomError
from utils.helpers import years_diff
from utils.constants import user_titles


class GuardianSchema(UserSchema):
    class Meta:
        model = Guardian
        load_instance = True

    # Guardian specific schema
    title = fields.Str(validate=validate.OneOf([*user_titles]), required=True)

    @validates("date_of_birth")
    def validate_dob(self, dob: str):
        if years_diff(dob) < 16:
            raise CustomError("Date of birth should be at least 16 years ago")
