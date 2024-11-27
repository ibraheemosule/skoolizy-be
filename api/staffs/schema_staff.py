from api.staffs.model_staffs import Staff
from configs.db.base_schemas.user_schema import UserSchema


class StaffSchema(UserSchema):
    class Meta:
        model = Staff
        load_instance = True
