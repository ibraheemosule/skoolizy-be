from flask import Blueprint

from .controllers_account import AccountControllers

account = AccountControllers()

account_bp = Blueprint("account", __name__)


@account_bp.route("/account", methods=["GET"])
def get_account():
    return account.get()


@account_bp.route("/account", methods=["DELETE"])
def delete_account():
    return account.delete()


@account_bp.route("/account", methods=["PATCH"])
def update_account():
    return account.update()
