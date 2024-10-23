from datetime import datetime, timedelta, timezone
from flask import jsonify, make_response
from utils.error_handlers import CustomError
import os
from redis_client import cache
from .auth_typings import TUserAuth
import jwt
from redis_client import cache
from utils.email_utils import send_email


def generate_refresh_token(user_id: TUserAuth):
    """Generate refresh tokens"""
    REFRESH_TOKEN_EXPIRES_DAYS = os.getenv('REFRESH_TOKEN_EXPIRES_DAYS')

    refresh_token = jwt.encode(
        {**user_id, 'exp': datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS)},
        os.getenv('JWT_SECRET_KEY'),
        algorithm="HS256",
    )

    cache.setex(user_id['tag'], REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60, refresh_token)
    return refresh_token


def generate_access_token(user_id: TUserAuth):
    """Generate access tokens"""

    access_token = jwt.encode(
        {**user_id, 'exp': datetime.now(timezone.utc) + timedelta(minutes=os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES"))},
        os.getenv('JWT_SECRET_KEY'),
        algorithm="HS256",
    )

    return access_token


def decode_token(token):
    """Verify and decode a JWT token."""

    try:
        return jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"], options={"verify_exp": True})
    except jwt.ExpiredSignatureError:
        return 'expired'
    except jwt.InvalidTokenError:
        return 'invalid'


def generate_tokens_and_response(user_id: TUserAuth, status_code=200):
    """Generate token and send json response"""

    response = make_response(
        jsonify({"data": {"tag": user_id.get("tag"), "access_token": generate_access_token(user_id=user_id)}}),
        status_code,
    )

    response.set_cookie("refresh_token", generate_refresh_token(user_id), httponly=True)
    return response


def generate_otp(*, recipient: str, email_title: str):
    """Generate otp and send to email"""
    cache.delete(recipient)
    if cache.get(recipient):
        return "Previous OTP sent is still valid"

    from random import random
    from math import ceil

    otp = ceil(random() * 1000000)

    message = f"Your OTP is {otp}"
    send_email(recipients=[recipient], subject=email_title, message=message)

    print(os.getenv('OTP_EXPIRY_TIME_IN_MINUTES'))
    cache.setex(recipient, int(os.getenv('OTP_EXPIRY_TIME_IN_MINUTES')) * 60, otp)

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
