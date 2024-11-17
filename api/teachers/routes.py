from flask import Blueprint
from .controllers import Teachers

teachers = Teachers()

teachers_bp = Blueprint("teachers", __name__)


@teachers_bp.route("/teachers/<string:id>", methods=["GET"])
def get_by_id_teachers(id: str):
    return teachers.get_one(id)


@teachers_bp.route("/teachers", methods=["GET"])
def get_teachers():
    return teachers.get_all()


@teachers_bp.route("/teachers/<string:tag>", methods=["DELETE"])
def delete_teacher(tag: str):
    return teachers.delete(tag)


@teachers_bp.route("/teachers/<string:tag>", methods=["PUT"])
def update_teacher(tag: str):
    return teachers.update(tag)
