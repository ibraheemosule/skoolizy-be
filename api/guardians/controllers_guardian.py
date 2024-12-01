from flask import Response, request
from sqlalchemy import or_
from configs.db import db
from utils.error_handlers import CustomError
from utils.helpers import format_date_time, model_to_dict, today_date
from .schema_guardian import GuardianSchema
from .constants_guardians import fields, private_fields
from .model_guardians import Guardian

from utils.success_handlers import res, res_paginated

schema = GuardianSchema(session=db.session)


class GuardianControllers:
    def get_all(self) -> Response:
        '''Gets all the guardians'''
        req = request.args.get

        page = int(req('page', 1))
        per_page = int(req('per_page', 10))
        date_joined = req("date_joined")

        query = Guardian.query

        if name := req("name"):
            query = query.filter(or_(Guardian.first_name.ilike(f"%{name}%"), Guardian.last_name.ilike(f"%{name}%")))
        if tier := req("tier"):
            query = query.filter(Guardian.tier == tier)
        if gender := req("gender"):
            query = query.filter(Guardian.gender == gender)
        if date_joined:
            date_joined = format_date_time(date_joined)["datetime_parse"]

            if date_joined > today_date():
                raise CustomError("Date joined should not be a future date")
            query = query.filter(Guardian.created_at.between(date_joined, today_date()))

        schema = GuardianSchema(many=True, only=["first_name", "middle_name", "last_name", "group", "tag"])

        return res_paginated(schema=schema, query=query, per_page=per_page, page=page, list_type="Guardian")

    def create(self) -> Response:
        """Sign up a user"""
        data = request.get_json()

        validated_guardian = schema.load(data)
        db.session.add(validated_guardian)
        db.session.commit()

        scoped_schema = GuardianSchema(
            session=db.session, only=["tag", "email", "verified", "tier", "first_name", "last_name", "group"]
        )
        return scoped_schema.dump(validated_guardian)

    def get_one(self, query_tag: str = None, user_req: bool = False) -> Response:
        '''Will work on this later'''
        tag = request.session_user['tag'] if user_req else query_tag

        guardian = Guardian.query.filter_by(tag=tag).first()

        if guardian == None:
            raise CustomError(f"{tag} does not exist")

        fields_to_send = [field for field in fields if field not in private_fields]

        schema = GuardianSchema(session=db.session, only=(None if user_req else [*fields_to_send]))

        return res(message="data retrieved successfully", data=schema.dump(guardian))

    def update(self, query_tag: str = None, user_req: bool = False) -> Response:
        '''Updates a guardian information'''

        data = request.get_json()

        if len(data.keys()) == 0:
            raise CustomError("No payload was sent")

        session_user = request.session_user
        tag = session_user['tag'] if user_req else query_tag

        guardian = Guardian.query.filter_by(tag=tag).first()

        guardian_dict = {**model_to_dict(guardian), **data}
        del guardian_dict['tag']
        if not user_req:
            raise CustomError("Invalid request made to route", 403)

        if query_tag != session_user['tag']:
            for field in private_fields:
                if field in data:
                    raise CustomError(f"Only account owner can modify {field} field")

        validated_guardian = schema.load(guardian_dict)

        Guardian.update(schema.dump(validated_guardian), tag)

        return res(message=f"{tag} details with has been updated")

    def delete(self, query_tag: str, user_req: bool = False) -> Response:
        '''Deletes a Guardian'''

        tag = request.session_user['tag'] if user_req else query_tag

        guardian = Guardian.query.filter_by(tag=tag).first()

        if guardian == None:
            raise CustomError(f"{tag} does not exist")

        if not user_req:
            raise CustomError("You are not authorized to delete this account")

        db.session.delete(guardian)
        return res(message=f"{tag} has been deleted successfully")
