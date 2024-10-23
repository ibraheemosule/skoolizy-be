from flask import Blueprint
from .controllers import Auth

auth = Auth()

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/send-otp", methods=["POST"])
def send_otp():
    return auth.send_otp()


@auth_bp.route("/auth/refresh-token", methods=["GET"])
def refresh_token():
    return auth.refresh_token()
