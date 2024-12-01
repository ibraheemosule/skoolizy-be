from flask import Blueprint
from .controllers_guardian import GuardianControllers

guardians = GuardianControllers()

guardians_bp = Blueprint("guardians", __name__)


@guardians_bp.route("/guardians/<string:tag>", methods=["GET"])
def get_guardian_by_tag(tag: str):
    return guardians.get_one(query_tag=tag)


@guardians_bp.route("/guardians", methods=["GET"])
def get_guardians():
    return guardians.get_all()


@guardians_bp.route("/guardians/<string:tag>", methods=["DELETE"])
def delete_guardian(tag: str):
    return guardians.delete(query_tag=tag)


@guardians_bp.route("/guardians/<string:tag>", methods=["PUT"])
def update_guardian(tag: str):
    return guardians.update(query_tag=tag)
