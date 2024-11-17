from flask import Response, request

from configs.envs import FRONTEND_URL, EMAIL
from configs.db import db
from .validations import teacher_validation
from .data_types import TTeacherPayload
from utils.error_handlers import CustomError
from .models import Teacher, TeacherSchema

from utils.success_handlers import res


class Teachers:
    def get_all(self) -> Response:
        '''Gets all the teachers'''
        teacher = Teacher.query.all()
        schema = TeacherSchema(many=True, only=["first_name", "middle_name", "last_name", "role", "tag"])

        return res(data={"message": "data retrieved successfully", "data": schema.dump(teacher)})

    def create(self) -> Response:
        """Sign up a user"""
        data = request.json

        last_id = getattr(Teacher.query.order_by(Teacher.id.desc()).first(), 'get_id', lambda: 0)()
        tag = f'staff-{last_id + 1}'

        data["tag"] = tag

        schema = TeacherSchema()
        validated_teacher = schema.load(data, session=Teacher)
        db.session.add(validated_teacher)
        db.session.commit()

        return tag

    def get_one(self, tag: str) -> Response:
        '''Will work on this later'''

        teacher = Teacher.query.filter_by(tag=tag).first()
        if teacher == None:
            raise CustomError(f"{tag} does not exist")

        schema = TeacherSchema()
        return res(data={"message": "data retrieved successfully", "data": schema.dump(teacher)})

    def update(self, tag: str) -> Response:
        '''Updates a teacher information'''

        data = request.json

        if len(data.keys()) == 0:
            raise CustomError("No payload was sent")

        schema = TeacherSchema()
        schema.load(data, partial=True, session=Teacher)

        teacher: Teacher = db.session.get(Teacher, tag)

        immutables = ("state_of_origin", "date_of_birth")
        for value in data.keys():
            if value in immutables:
                raise CustomError(f"Cannot modify {value}", 403)

        for key, value in data.item():
            if hasattr(teacher, key):
                setattr(teacher, key, value)

        db.session.commit()

        return res(data={"message": f"{teacher.tag} details with has been updated"})

    def delete(self, tag: str) -> Response:
        '''Deletes a teacher information'''

        teacher = Teacher.query.filter_by(tag=tag).first()

        if teacher == None:
            raise CustomError(f"{tag} does not exist")

        db.session.delete(teacher)
        return res(data={"message": f"{tag} has been deleted successfully"})
