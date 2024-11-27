from flask import Response, request
from sqlalchemy import or_

from configs.envs import FRONTEND_URL, EMAIL
from configs.db import db
from utils.error_handlers import CustomError
from utils.helpers import format_date_time, model_to_dict, parse_date, today_date
from .schema_staff import StaffSchema
from .model_staffs import Staff

from utils.success_handlers import res, res_paginated

schema = StaffSchema(session=db.session)


class StaffControllers:
    def get_all(self) -> Response:
        '''Gets all the staffs'''
        req = request.args.get

        page = int(req('page', 1))
        per_page = int(req('per_page', 10))
        date_joined = req("date_joined")

        query = Staff.query

        if name := req("name"):
            query = query.filter(or_(Staff.first_name.ilike(f"%{name}%"), Staff.last_name.ilike(f"%{name}%")))
        if tier := req("tier"):
            query = query.filter(Staff.tier == tier)
        if gender := req("gender"):
            query = query.filter(Staff.gender == gender)
        if date_joined:
            date_joined = format_date_time(date_joined)["datetime_parse"]

            if date_joined > today_date():
                raise CustomError("Date joined should not be a future date")
            query = query.filter(Staff.created_at.between(date_joined, today_date()))

        schema = StaffSchema(many=True, only=["first_name", "middle_name", "last_name", "group", "tag"])

        return res_paginated(schema=schema, query=query, per_page=per_page, page=page, list_type="Staff")

    def create(self) -> Response:
        """Sign up a user"""
        data = request.get_json()

        validated_staff = schema.load(data)
        db.session.add(validated_staff)
        db.session.commit()

        scoped_schema = StaffSchema(session=db.session, only=["tag", "email", "verified", "tier"])
        return scoped_schema.dump(validated_staff)

    def get_one(self, tag: str) -> Response:
        '''Will work on this later'''

        staff = Staff.query.filter_by(tag=tag).first()
        if staff == None:
            raise CustomError(f"{tag} does not exist")

        return res(message="data retrieved successfully", data=schema.dump(staff))

    def update(self, tag: str) -> Response:
        '''Updates a staff information'''

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
        '''Deletes a Staff'''

        staff = Staff.query.filter_by(tag=tag).first()

        if staff == None:
            raise CustomError(f"{tag} does not exist")

        db.session.delete(staff)
        return res(message=f"{tag} has been deleted successfully")
