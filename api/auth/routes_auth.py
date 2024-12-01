from flask import Blueprint
from .controllers_auth import Auth

auth = Auth()

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    return auth.signup()


@auth_bp.route('/auth/verify-account', methods=['PATCH'])
def confirm_signup():
    return auth.verify_account()


@auth_bp.route('/auth/signin', methods=['POST'])
def signin():
    return auth.signin()


@auth_bp.route("/auth/send-code", methods=["POST"])
def send_otp():
    return auth.send_otp()


@auth_bp.route("/auth/refresh-token", methods=["GET"])
def refresh_token():
    return auth.refresh_token()


@auth_bp.route("/auth/send-reset-password-link/<string:tag>", methods=["GET"])
def generate_reset_password_link(tag: str):
    return auth.generate_reset_password_link(tag)


@auth_bp.route("/auth/create-new-password", methods=["PUT"])
def reset_password():
    return auth.create_new_password()
