from flask import Response, request, jsonify
from utils.auth import generate_otp, decode_token, generate_access_token
from utils.email_utils import is_email_valid
from utils.auth.auth_typings import TUserAuth
from typing import Union


class Auth:
    def send_otp(self) -> Response:
        data = request.json
        email = data.get('email')

        if is_email_valid(email):
            return jsonify({"data": {"message": generate_otp(recipient=email, email_title="OTP from Skoolizy")}})

        return jsonify({"data": {"message": "Invalid email payload"}})

    def refresh_token(self) -> Response:
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            return jsonify({"data": {"message": "Token is missing"}})

        decoded_token: Union[TUserAuth, str] = decode_token(refresh_token)

        if decoded_token == 'expired':
            return jsonify({"data": {"message": "Token expired"}})

        if decoded_token == 'invalid':
            return jsonify({"data": {"message": "Token is invalid"}})

        return jsonify({"data": {"access_token": generate_access_token(user_id=decoded_token["tag"])}})
