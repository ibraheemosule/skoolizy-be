from flask import Response, request
from api.staffs.controllers_staff import StaffControllers
from api.staffs.model_staffs import Staff
from configs.envs import ACCESS_TOKEN_EXPIRES_MINUTES, EMAIL, FRONTEND_URL
from configs.db import db
from utils.auth import generate_otp, decode_token, generate_access_token, generate_tokens_and_response, verify_code
from utils.email_utils import is_email_valid, send_email
from utils.auth.auth_typings import TUserAuth
from typing import Union
from utils.error_handlers import CustomError
from utils.success_handlers import res
from utils.constants import groups
from configs.redis_client import cache
from utils.get_html import default_html


class Auth:
    def signup(self) -> Response:
        group = request.get_json().get('group')

        if group not in groups:
            raise CustomError("Invalid group provided")

        if group == 'staffs':
            staffs = StaffControllers()
            user = staffs.create()

        message = f"""
        <p>Hi {user.get('first_name')},</p>

        <p>Your account has been successfully created!</p>

        <strong>Your Tag is {user.get('tag')}.</strong>

        <p>Use it to <a href={FRONTEND_URL}/auth/login target="_blank">log in</a> and start exploring all that we offer.\n
        If you have any questions, feel free to reach out to our <a href="mailto:{EMAIL}">support team</a>.</p>

        <p>Thanks for joining us!</p>
        """

        send_email(
            subject="Account Created on Skoolizy",
            message=default_html(message=message, title="Welcome to Skoolizy"),
            recipients=[user.get('email')],
        )

        response_data = {
            "access_token": generate_access_token(user_id=user),
            "verified": user['verified'],
            "tag": user['tag'],
            "email": user['email'],
            "group": user["group"],
        }

        return generate_tokens_and_response(action_text="Sign up", user_id=response_data)

    def verify_account(self) -> Response:
        session_user = request.session_user
        tag: str = session_user.get('tag')

        if tag == None:
            raise CustomError("No tag provided")

        user = None

        if tag.count('staff'):
            user: Staff = Staff.query.filter_by(tag=tag).first()

        if user == None:
            raise CustomError(f"Account associated with tag-{tag} is not found")

        if user.verified:
            raise CustomError(f"Account with tag-{tag} is already verified")

        verify = verify_code(code=request.json.get('code'), recipient=user.email)

        if not verify:
            raise CustomError("Unable to verify code", 403)

        user.verified = True
        db.session.commit()

        return res(message="Account verification successful")

    def signin(self) -> Response:
        data = request.json
        tag = data.get("tag")
        password = data.get("password")

        if not tag:
            raise CustomError('Tag is required', 404)

        user = None

        if tag.count("staff"):
            user: Staff = Staff.query.filter_by(tag=tag).first()

        if not user:
            raise CustomError(f'Account with {tag} unknown', 404)

        if not user.check_password(password=password):
            raise CustomError("Password is incorrect")

        response_data = {
            "verified": user.verified,
            "tag": user.tag,
            "tier": user.tier,
            "email": user.email,
            "group": user.group,
        }

        return generate_tokens_and_response(user_id=response_data)

    def send_otp(self) -> Response:
        session_user = request.session_user
        email = session_user.get('email')

        if is_email_valid(email):
            send_status = generate_otp(recipient=email, email_title="OTP from Skoolizy")

            return res(message=send_status)

        raise CustomError("Invalid email payload")

    def refresh_token(self) -> Response:
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            raise CustomError("Expired token")

        decoded_token: Union[TUserAuth, str] = decode_token(token=refresh_token)

        return res(
            message="Token refresh successful", data={"access_token": generate_access_token(user_id=decoded_token)}
        )

    def generate_reset_password_link(self, tag: str) -> Response:
        '''Generate a link that is sent to the user email for resetting password'''

        staff: Staff = Staff.query.filter_by(tag=tag).first()

        if not staff:
            raise CustomError("No user with tag found")

        token = generate_access_token(user_id={f"reset_{tag}": tag})

        link = f"{FRONTEND_URL}/auth/reset-password?token={token}"

        message = f"""A request has been made to reset your password.\n
        If this was initated by you, Please click this 
        <a href="{link}" target="_blank">link</a>"""

        send_email(
            subject="Reset your password",
            message=default_html(message=message, title="Password Reset Link"),
            recipients=[staff.email],
        )

        cache.setex(name=token, value="unused", time=ACCESS_TOKEN_EXPIRES_MINUTES * 60)

        return res(message=f"A reset password link has been sent to {tag} email")

    def create_new_password(self) -> Response:
        '''Creates a new password, if the link is valid and the password provided are valid'''

        data = request.json
        token = data.get('token')
        new_password = data.get('new_password')

        if new_password == None:
            raise CustomError('No new password payload provided')

        if cache.get(token) == None:
            raise CustomError('Reset password link is invalid')

        if cache.get(token) == 'used':
            raise CustomError('Reset password link has been used!', 409)

        from utils.helpers import is_password_valid

        if not is_password_valid(new_password):
            raise CustomError(
                "Password must be at least 8 chars long and must contain one uppercase letter, one lowercase letter, one number and one symbol"
            )

        decoded_token: str = decode_token(token=token, err_message="password link")

        tag = decoded_token[list(decoded_token.keys())[0]]

        staff: Staff = Staff.query.filter_by(tag=tag).first()
        staff.password = new_password

        db.session.commit()

        message = f"""Your account password has been reset successfully.\n
        You have been logged out of all sessions. You can <a href={FRONTEND_URL} target="_blank">Log in here</a>"""

        send_email(
            subject="Password reset notificaton",
            message=default_html(message=message, title="Password Reset Successful"),
            recipients=[staff.email],
        )

        cache.setex(name=token, value="used", time=ACCESS_TOKEN_EXPIRES_MINUTES * 60)

        return res(message="Password reset successfully")
