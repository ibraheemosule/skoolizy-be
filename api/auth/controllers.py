from flask import Response, request
from utils.auth import generate_otp, decode_token, generate_access_token, generate_tokens_and_response, verify_otp
from utils.email_utils import is_email_valid
from utils.auth.auth_typings import TUserAuth
from typing import Union
from utils.error_handlers import CustomError
from utils.success_handlers import res


class Auth:
    def signup(self) -> Response:
        data = request.json

        if data.get('role') == 'staff':
            from api.teachers.controllers import Teachers

            teachers = Teachers()
            return teachers.signup(data=data)

        raise CustomError("Invalid role provided")

    def confirm_signup(self) -> Response:
        print(request.json)
        data = request.json
        email = data.get("email")

        verify = verify_otp(otp=data.get('otp'), recipient=email)

        if verify:
            from api.teachers.controllers import Teachers

            teachers = Teachers()
            return teachers.confirm_signup(email)

        raise CustomError("Unable to confirm signup!", 403)

    def signin(self) -> Response:
        data = request.json
        tag = data.get("tag")
        password = data.get("password")

        from api.teachers.models import Teacher

        teacher: Teacher = Teacher.query.filter_by(tag=tag).first()

        if not teacher:
            raise CustomError(f"Account with {tag} not found", 404)

        if not teacher.check_password(password=password):
            raise CustomError("Password is incorrect")

        return generate_tokens_and_response(user_id={"tag": teacher.tag})

    def send_otp(self) -> Response:
        data = request.json
        email = data.get('email')

        if is_email_valid(email):
            return res(data={"message": generate_otp(recipient=email, email_title="OTP from Skoolizy")})
        raise CustomError("Invalid email payload")

    def refresh_token(self) -> Response:
        refresh_token = request.cookies.get('refresh_token')
        print(request.cookies)

        if not refresh_token:
            raise CustomError("Token is missing")

        decoded_token: Union[TUserAuth, str] = decode_token(token=refresh_token)

        return res(data={"access_token": generate_access_token(user_id=decoded_token)})

    def generate_reset_password_link(self, tag: str) -> Response:
        '''Generate a link that is sent to the user email for resetting password'''

        from api.teachers.models import Teacher

        teacher: Teacher = Teacher.query.filter_by(tag=tag).first()

        if not teacher:
            raise CustomError("No user with tag found")

        token = generate_access_token(user_id={f"reset_{tag}": tag})

        import os

        link = f"{os.getenv('FRONTEND_URL')}/auth/reset-password?token={token}"

        message = f"""A request has been made to reset your password.\n
        If this was initated by you, Please click this 
        <a href="{link}" target="_blank">link</a>"""

        from utils.get_html import get_email

        content = (
            get_email('boilerplate.html').replace("{{message}}", message).replace("{{title}}", "Password Reset Link")
        )

        from utils.email_utils import send_email

        send_email(subject="Reset your password", message=content, recipients=[teacher.email])

        return res(data={"message": f"A reset password link has been sent to {tag} email"})

    def create_new_password(self) -> Response:
        '''Creates a new password, if the link is valid and the password provided are valid'''

        data = request.json
        token = data.get('token')
        new_password = data.get('new_password')

        if not token:
            raise CustomError('Reset password link is invalid')

        if not new_password:
            raise CustomError('No new password payload provided')

        from utils.helpers import is_password_valid

        if not is_password_valid(new_password):
            raise CustomError(
                "Password must be at least 8 chars long and must contain one uppercase letter, one lowercase letter, one number and one symbol"
            )

        decoded_token: str = decode_token(token=token, err_message="password link")

        tag = decoded_token[list(decoded_token.keys())[0]]

        from api.teachers.models import Teacher

        teacher: Teacher = Teacher.query.get(tag)
        teacher.set_password(password=new_password)

        from db import db

        db.session.commit()

        return res(data={"message": "Password reset successfully"})
