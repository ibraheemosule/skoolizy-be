from flask import Response, request
from api.staffs.model_staffs import Staff
from api.staffs.schema_staff import StaffSchema
from configs.db import db
from utils.error_handlers import CustomError
from utils.helpers import model_to_dict
from utils.success_handlers import res


schema = StaffSchema(session=db.session)


class AccountControllers:
    def get(self, tag: str) -> Response:
        '''Get account information'''

        staff = Staff.query.filter_by(tag=tag).first()
        if staff == None:
            raise CustomError(f"{tag} does not exist")

        return res(message="data retrieved successfully", data=schema.dump(staff))

    def update(self, tag: str) -> Response:
        '''Updates account information'''

        data = request.json

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
