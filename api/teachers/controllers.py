from datetime import datetime
from flask import Response, request
from sqlalchemy import or_

from configs.envs import FRONTEND_URL, EMAIL
from configs.db import db
from utils.error_handlers import CustomError
from utils.helpers import parse_date, today_date
from .models import Teacher, TeacherSchema

from utils.success_handlers import res, res_paginated

schema = TeacherSchema(session=db.session)


class Teachers:
    def get_all(self) -> Response:
        '''Gets all the teachers'''
        req = request.args.get

        page = int(req('page', 1))
        per_page = int(req('per_page', 10))
        date_joined = req("date_joined")

        query = Teacher.query

        if name := req("name"):
            query = query.filter(or_(Teacher.first_name.ilike(f"%{name}%"), Teacher.last_name.ilike(f"%{name}%")))
        if tier := req("tier"):
            query = query.filter(Teacher.tier == tier)
        if gender := req("gender"):
            query = query.filter(Teacher.gender == gender)
        if date_joined:
            date_joined = parse_date(date_joined)

            if date_joined > today_date():
                raise CustomError("Date joined should not be a future date")
            query = query.filter(Teacher.created_at.between(date_joined, today_date()))

        schema = TeacherSchema(many=True, only=["first_name", "middle_name", "last_name", "role", "tag"])

        return res_paginated(schema=schema, query=query, per_page=per_page, page=page, list_type="Staff")

    def create(self) -> Response:
        """Sign up a user"""
        data = request.json

        validated_teacher = schema.load(data)
        db.session.add(validated_teacher)
        db.session.commit()

        return schema.dump(validated_teacher).get('tag')

    def get_one(self, tag: str) -> Response:
        '''Will work on this later'''

        teacher = Teacher.query.filter_by(tag=tag).first()
        if teacher == None:
            raise CustomError(f"{tag} does not exist")

        return res(message="data retrieved successfully", data=schema.dump(teacher))

    def update(self, tag: str) -> Response:
        '''Updates a teacher information'''

        data = request.json

        if len(data.keys()) == 0:
            raise CustomError("No payload was sent")

        validated_teacher = schema.load(data, partial=True)

        Teacher.update(schema.dump(validated_teacher), tag)

        return res(message=f"{tag} details with has been updated")

    def delete(self, tag: str) -> Response:
        '''Deletes a teacher information'''

        teacher = Teacher.query.filter_by(tag=tag).first()

        if teacher == None:
            raise CustomError(f"{tag} does not exist")

        db.session.delete(teacher)
        return res(message=f"{tag} has been deleted successfully")
