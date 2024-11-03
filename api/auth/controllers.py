from flask import Response, request
from api.teachers.models import Teacher
from configs import envs
from utils.auth import generate_otp, decode_token, generate_access_token, generate_tokens_and_response, verify_otp
from utils.email_utils import is_email_valid, send_email
from utils.auth.auth_typings import TUserAuth
from typing import Union
from utils.error_handlers import CustomError
from utils.success_handlers import res
from configs.redis_client import cache
from utils.get_html import default_html


class Auth:
    def signup(self) -> Response:
        data = request.json

        if data.get('role') == 'staff':
            from api.teachers.controllers import Teachers

            teachers = Teachers()
            response, message = teachers.signup(data=data)

            send_email(
                subject="Account Created on Skoolizy",
                message=default_html(message=message, title="Welcome to Skoolizy"),
                recipients=[data.get('email')],
            )

            return response

        raise CustomError("Invalid role provided")

    def confirm_signup(self) -> Response:
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
            # teacher: Teacher = Teacher.query.filter_by(email=email).first()

            # if not teacher:
            #         raise CustomError(f"Account with {tag} not found", 404)

            send_status = generate_otp(recipient=email, email_title="OTP from Skoolizy")

            return res(data={"message": send_status})

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

        link = f"{envs.FRONTEND_URL}/auth/reset-password?token={token}"

        message = f"""A request has been made to reset your password.\n
        If this was initated by you, Please click this 
        <a href="{link}" target="_blank">link</a>"""

        send_email(
            subject="Reset your password",
            message=default_html(message=message, title="Password Reset Link"),
            recipients=[teacher.email],
        )

        cache.setex(name=token, value="unused", time=envs.ACCESS_TOKEN_EXPIRES_MINUTES * 60)

        return res(data={"message": f"A reset password link has been sent to {tag} email"})

    def create_new_password(self) -> Response:
        '''Creates a new password, if the link is valid and the password provided are valid'''

        data = request.json
        token = data.get('token')
        new_password = data.get('new_password')

        if cache.get(token) == 'used':
            raise CustomError('Reset password link has been used!', 409)

        if not cache.get(token):
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

        teacher: Teacher = Teacher.query.filter_by(tag=tag).first()
        teacher.set_password(password=new_password)

        from configs.db import db

        db.session.commit()

        import os

        message = f"""Your account password has been reset successfully.\n
        You have been logged out of all sessions. You can <a href={envs.FRONTEND_URL} target="_blank">Log in here</a>"""

        send_email(
            subject="Password reset notificaton",
            message=default_html(message=message, title="Password Reset Successful"),
            recipients=[teacher.email],
        )

        cache.setex(name=token, value="used", time=envs.ACCESS_TOKEN_EXPIRES_MINUTES * 60)

        return res(data={"message": "Password reset successfully"})
