from datetime import datetime, timedelta, timezone
from flask import make_response, request
from configs import envs
from utils.error_handlers import CustomError
import os
from configs.redis_client import cache
from .auth_typings import TUserAuth
import jwt
from utils.email_utils import send_email
from utils.success_handlers import res


def generate_refresh_token(user_id: TUserAuth):
    """Generate refresh tokens"""

    refresh_token = jwt.encode(
        {**user_id, 'exp': datetime.now(timezone.utc) + timedelta(days=envs.REFRESH_TOKEN_EXPIRES_DAYS)},
        envs.JWT_SECRET_KEY,
        algorithm="HS256",
    )

    cache.setex(user_id['tag'], envs.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60, refresh_token)
    return refresh_token


def generate_access_token(user_id: TUserAuth):
    """Generate access tokens"""

    access_token = jwt.encode(
        {
            **user_id,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=envs.ACCESS_TOKEN_EXPIRES_MINUTES),
        },
        envs.JWT_SECRET_KEY,
        algorithm="HS256",
    )

    return access_token


def decode_token(*, token, err_message="token"):
    """Verify and decode a JWT token."""

    try:
        return jwt.decode(token, envs.JWT_SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True})
    except jwt.ExpiredSignatureError:
        raise CustomError(f"Expired {err_message}")
    except jwt.InvalidTokenError:
        raise CustomError(f"Invalid {err_message}")


def generate_tokens_and_response(user_id: TUserAuth, status_code=200):
    """Generate token and send json response"""

    response = make_response(
        res(
            data={"tag": user_id.get("tag"), "access_token": generate_access_token(user_id=user_id)},
            status_code=status_code,
        ),
    )

    response.set_cookie(
        key="refresh_token", value=generate_refresh_token(user_id), httponly=True, secure=True, samesite='Strict'
    )
    return response


def generate_otp(*, recipient: str, email_title: str):
    """Generate otp and send to email"""

    if cache.get(recipient):
        return "Previous OTP sent is still valid"

    from random import random
    from math import ceil

    otp = ceil(random() * 1000000)

    from utils.get_html import default_html

    html_message = f"Hi, <div>Your code is <strong>{str(otp)}</strong></div> <div>This code expires in 5 minutes</div>"

    send_email(
        recipients=[recipient],
        subject=email_title,
        message=default_html(title="Code from Skoolizy", message=html_message),
    )

    cache.setex(recipient, envs.OTP_EXPIRY_TIME_IN_MINUTES * 60, otp)

    return f"OTP has been sent to {recipient}"


def verify_otp(*, otp: int, recipient: str):
    """Verify the otp sent to email"""

    if not otp:
        raise CustomError("No OTP payload received", 403)

    cached_otp = cache.get(recipient)
    if not cached_otp:
        raise CustomError("OTP has expired, please request again", 403)

    if cached_otp == otp:
        cache.delete(recipient)
        return True
    else:
        return False


def protected_route(func):
    def checker(*args, **kwargs):
        if 'Authorization' not in request.headers:
            raise CustomError("Access token is missing", 401)

        token = request.headers['Authorization'].split(' ')

        if token[0] != 'Bearer' or not token[1]:
            raise CustomError('Invalid token format provided')

        kwargs["user"] = decode_token(token=token[1])
        return func(*args, **kwargs)

    return checker
