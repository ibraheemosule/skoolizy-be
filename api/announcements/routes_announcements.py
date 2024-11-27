from flask import Blueprint
from .controllers_announcements import Announcements
from utils.auth import set_session

announcements = Announcements()

announcements_bp = Blueprint("announcements", __name__)


@announcements_bp.before_request
def protect_routes():
    set_session()


@announcements_bp.route("/announcements/<string:id>", methods=["GET"])
def get_by_id_announcements(id: str):
    return announcements.get_one(id)


@announcements_bp.route("/announcements", methods=["GET"])
def get_announcements():
    return announcements.get()


@announcements_bp.route("/announcements", methods=["POST"])
def post_announcements(session_user):
    return announcements.post(session_user)


@announcements_bp.route("/announcements/<string:id>", methods=["DELETE"])
def delete_announcement(id: str):
    return announcements.delete(id)


@announcements_bp.route("/announcements/<string:id>", methods=["PUT"])
def update_announcement(id: str):
    return announcements.update(id)


@announcements_bp.route("/announcements/stop-reminder/<string:id>", methods=["PATCH"])
def stop_reminder(id: str):
    return announcements.stop_reminder(id)
