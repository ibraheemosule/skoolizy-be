from flask import Blueprint
from .controllers import Announcements

announcements = Announcements()

announcements_bp = Blueprint("announcements", __name__)


@announcements_bp.route("/announcements/<string:id>", methods=["GET"])
def get_by_id_announcements(id: str):
    return announcements.get_one(id)


@announcements_bp.route("/announcements", methods=["GET"])
def get_announcements():
    return announcements.get()


@announcements_bp.route("/announcements", methods=["POST"])
def post_announcements():
    return announcements.post()


@announcements_bp.route("/announcements/<string:id>", methods=["DELETE"])
def delete_announcement(id: str):
    return announcements.delete(id)


@announcements_bp.route("/announcements/<string:id>", methods=["PUT"])
def update_announcement(id: str):
    return announcements.update(id)
