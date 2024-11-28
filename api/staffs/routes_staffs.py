from flask import Blueprint

from utils.auth import set_session
from .controllers_staff import StaffControllers

staffs = StaffControllers()

staffs_bp = Blueprint("staffs", __name__)


@staffs_bp.before_request
def protect_routes():
    set_session()


@staffs_bp.route("/staffs/<string:tag>", methods=["GET"])
def get_staff_by_tag(tag: str):
    return staffs.get_one(query_tag=tag)


@staffs_bp.route("/staffs", methods=["GET"])
def get_staffs():
    return staffs.get_all()


@staffs_bp.route("/staffs/<string:tag>", methods=["DELETE"])
def delete_staff(tag: str):
    return staffs.delete(query_tag=tag)


@staffs_bp.route("/staffs/<string:tag>", methods=["PUT"])
def update_staff(tag: str):
    return staffs.update(query_tag=tag)
