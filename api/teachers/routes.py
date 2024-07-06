from flask import Blueprint
from .controllers import Teachers

teachers = Teachers()

teachers_bp = Blueprint("teachers", __name__)


@teachers_bp.route("/teachers/<string:id>", methods=["GET"])
def get_by_id_teachers(id: str):
    return teachers.get_one(id)


@teachers_bp.route("/teachers", methods=["GET"])
def get_teachers():
    return teachers.get()


@teachers_bp.route("/teachers", methods=["POST"])
def post_teachers():
    return teachers.post()


@teachers_bp.route("/teachers/<string:id>", methods=["DELETE"])
def delete_teacher(id: str):
    return teachers.delete(id)


@teachers_bp.route("/teachers/<string:id>", methods=["PUT"])
def update_teacher(id: str):
    return teachers.update(id)
