from flask import Response, request, jsonify
from .validations import teacher_validation
from .data_types import TTeacherPayload, TConfirmSignup
from utils.error_handlers import CustomError
from .models import Teacher
from werkzeug.security import generate_password_hash
from utils.auth import generate_tokens_and_response, generate_otp, verify_otp


class Teachers:
    def get(self) -> Response:
        '''Will work on this later'''
        pass

    def create(self) -> Response:
        data: TTeacherPayload = request.json

        teacher_validation(data, ['password'])

        password = data.get('password')

        if not password:
            raise CustomError("No password provided", 403)

        from .models import Teacher

        last_id = getattr(Teacher.query.order_by(Teacher.id.desc()).first(), 'get_id', lambda: 0)()
        tag = f'sf-{last_id + 1}'

        from db import db

        db.session.add(
            Teacher(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                middle_name=data.get("middle_name"),
                gender=data.get("gender"),
                date_of_birth=(data.get("date_of_birth")),
                country=(data.get("country")),
                state_of_origin=(data.get("state_of_origin")),
                email=(data.get("email")),
                tier=str(3),
                tag=tag,
                password_hash=generate_password_hash(data.get('password')),
            )
        )

        db.session.commit()
        send_otp = generate_otp(recipient=data.get("email"), email_title="OTP To Verify Account")

        return jsonify({"data": {"message": send_otp}})

    def get_one(self, id: str) -> Response:
        '''Will work on this later'''
        pass

    def update(self, id: str) -> Response:
        '''Will work on this later'''
        pass

    def delete(self, id: str) -> Response:
        '''Will work on this later'''
        pass

    def confirm_signup(self) -> Response:
        data: TConfirmSignup = request.json
        email = data.get('email')
        verify = verify_otp(otp=data.get('otp'), recipient=email)

        if verify:
            teacher: Teacher = Teacher.query.filter_by(email=email).first()
            teacher.verified = True

            from db import db

            db.session.commit()

            return generate_tokens_and_response(user_id={"tag": teacher.tag})

        raise CustomError("Invalid OTP, Try again!", 403)
