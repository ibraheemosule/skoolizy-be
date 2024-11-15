from flask import Response, request

from configs import envs
from .validations import teacher_validation
from .data_types import TTeacherPayload
from utils.error_handlers import CustomError
from .models import Teacher
from werkzeug.security import generate_password_hash
from utils.auth import generate_tokens_and_response
from utils.success_handlers import res
from utils.helpers import get_date_and_time


class Teachers:
    def get(self) -> Response:
        '''Will work on this later'''
        pass

    def signup(self, data: TTeacherPayload) -> Response:
        data = request.json

        # teacher_validation(data, ['password'])

        # password = data.get('password')

        # if not password:
        #     raise CustomError("No password provided", 403)

        last_id = getattr(Teacher.query.order_by(Teacher.id.desc()).first(), 'get_id', lambda: 0)()
        tag = f'staff-{last_id + 1}'

        from configs.db import db

        db.session.add(
            Teacher(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                middle_name=data.get("middle_name"),
                gender=data.get("gender"),
                date_of_birth=get_date_and_time(data.get("date_of_birth"))[0],
                phone_number=data.get('phone_number'),
                home_address=data.get('home_address'),
                country=(data.get("country")),
                state_of_origin=(data.get("state_of_origin")),
                email=(data.get("email")),
                tier=str(3),
                tag=tag,
                password_hash=generate_password_hash(data.get('password')),
                role=data.get('role'),
            )
        )

        db.session.commit()

        message = f"""
            Hi {data.get('first_name')},\n
            Your account has been successfully created!\n
            <strong>Your Tag is {tag}.</strong>\n
            Use it to <a href={envs.FRONTEND_URL}/auth/login target="_blank">log in<a> and start exploring all that we offer.\n
            If you have any questions, feel free to reach out to our <a href="mailto:{envs.EMAIL}">support team</a>.

            Thanks for joining us!"""

        return res(data={"message": "Sign up successful", "tag": tag}), message

    def get_one(self, id: str) -> Response:
        '''Will work on this later'''
        pass

    def update(self, id: str) -> Response:
        '''Will work on this later'''
        pass

    def delete(self, id: str) -> Response:
        '''Will work on this later'''
        pass

    def confirm_signup(self, email: str) -> Response:
        teacher: Teacher = Teacher.query.filter_by(email=email).first()
        teacher.verified = True

        from configs.db import db

        db.session.commit()

        return generate_tokens_and_response(user_id={"tag": teacher.tag})
