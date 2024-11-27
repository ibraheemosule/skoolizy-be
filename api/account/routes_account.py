from flask import Blueprint
from .controllers_account import AccountControllers

account = AccountControllers()

account_bp = Blueprint("account", __name__)


@account_bp.route("/account", methods=["GET"])
def get_account(tag: str):
    return account.get(tag)


@account_bp.route("/account", methods=["DELETE"])
def delete_account(tag: str):
    return account.delete(tag)


@account_bp.route("/account", methods=["PATCH"])
def update_account(tag: str):
    return account.update(tag)
