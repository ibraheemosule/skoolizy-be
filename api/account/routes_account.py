from flask import Blueprint

from utils.auth import set_session
from .controllers_account import AccountControllers

account = AccountControllers()

account_bp = Blueprint("account", __name__)


@account_bp.before_request
def protect_routes():
    set_session()


@account_bp.route("/account", methods=["GET"])
def get_account():
    return account.get()


@account_bp.route("/account", methods=["DELETE"])
def delete_account():
    return account.delete()


@account_bp.route("/account", methods=["PATCH"])
def update_account():
    return account.update()
