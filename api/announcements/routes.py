from flask import Blueprint
from .controllers import Announcements
from utils.auth import protected_route

announcements = Announcements()

announcements_bp = Blueprint("announcements", __name__)


@announcements_bp.route("/announcements/<string:id>", methods=["GET"])
def get_by_id_announcements(id: str):
    return announcements.get_one(id)


@announcements_bp.route("/announcements", methods=["GET"])
@protected_route
def get_announcements(user):
    return announcements.get()


@announcements_bp.route("/announcements", methods=["POST"])
@protected_route
def post_announcements(user):
    return announcements.post(user)


@announcements_bp.route("/announcements/<string:id>", methods=["DELETE"])
def delete_announcement(id: str):
    return announcements.delete(id)


@announcements_bp.route("/announcements/<string:id>", methods=["PUT"])
def update_announcement(id: str):
    return announcements.update(id)


@announcements_bp.route("/announcements/stop-reminder/<string:id>", methods=["PATCH"])
def stop_reminder(id: str):
    return announcements.stop_reminder(id)
