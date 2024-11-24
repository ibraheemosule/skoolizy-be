from flask import Response, request

from configs.envs import FRONTEND_URL, EMAIL
from configs.db import db
from utils.error_handlers import CustomError
from .models import Teacher, TeacherSchema

from utils.success_handlers import res

schema = TeacherSchema(session=db.session)


class Teachers:
    def get_all(self) -> Response:
        '''Gets all the teachers'''
        teacher = Teacher.query.all()
        schema = TeacherSchema(many=True, only=["first_name", "middle_name", "last_name", "role", "tag"])

        return res(data={"message": "data retrieved successfully", "data": schema.dump(teacher)})

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

        return res(data={"message": "data retrieved successfully", "data": schema.dump(teacher)})

    def update(self, tag: str) -> Response:
        '''Updates a teacher information'''

        data = request.json

        if len(data.keys()) == 0:
            raise CustomError("No payload was sent")

        validated_teacher = schema.load(data, partial=True)

        Teacher.update(schema.dump(validated_teacher), tag)

        return res(data={"message": f"{tag} details with has been updated"})

    def delete(self, tag: str) -> Response:
        '''Deletes a teacher information'''

        teacher = Teacher.query.filter_by(tag=tag).first()

        if teacher == None:
            raise CustomError(f"{tag} does not exist")

        db.session.delete(teacher)
        return res(data={"message": f"{tag} has been deleted successfully"})
