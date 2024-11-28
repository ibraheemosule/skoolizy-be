from flask import Response, request
from api.staffs.controllers_staff import StaffControllers
from api.staffs.model_staffs import Staff
from api.staffs.schema_staff import StaffSchema
from configs.db import db
from utils.error_handlers import CustomError
from utils.helpers import model_to_dict
from utils.success_handlers import res


schema = StaffSchema(session=db.session)


class AccountControllers:
    def get(self) -> Response:
        '''Get account information'''
        session_user = request.session_user
        tag = session_user['tag']

        if tag.count("staff"):
            staff = StaffControllers()
            return staff.get_one(user_req=True)

        staff = Staff.query.filter_by(tag=tag).first()
        if staff == None:
            raise CustomError(f"{tag} does not exist")

        return res(message="data retrieved successfully", data=schema.dump(staff))

    def update(self) -> Response:
        '''Updates account information'''
        tag = request.session_user['tag']

        data = request.get_json()

        if len(data.keys()) == 0:
            raise CustomError("No payload was sent")

        staff = Staff.query.filter_by(tag=tag).first()

        staff_dict = {**model_to_dict(staff), **data}
        del staff_dict['tag']

        validated_staff = schema.load(staff_dict)

        Staff.update(schema.dump(validated_staff), tag)

        return res(message=f"{tag} details with has been updated")

    def delete(self, tag: str) -> Response:
        '''Deletes Account'''

        staff = Staff.query.filter_by(tag=tag).first()

        if staff == None:
            raise CustomError(f"{tag} does not exist")

        db.session.delete(staff)
        return res(message=f"{tag} has been deleted successfully")
