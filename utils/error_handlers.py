from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError, OperationalError


class CustomError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def __error_response(*, error_type="client error", message, status_code):
    return jsonify({"error": error_type, "message": message}), status_code


def __db_errors(e: SQLAlchemyError):
    code, msg = e.orig.args

    """Handle duplicate value sent for unique field"""
    if code == 1062:
        start_index = msg.rfind('.') + 1
        end_index = msg.rfind("'")

        error_msg = msg[start_index : start_index + 1].upper() + msg[start_index + 1 : end_index]

        return __error_response(message=f"{error_msg} already exists", status_code=403)

    return jsonify({"error": "db error", "message": str(e.__cause__)}), 500


def __unhandled_errors(e):
    print(e)
    return __error_response(error_type="server error", message=str(e), status_code=500)


def __handle_type_errors(e: TypeError):
    print(e)
    return __error_response(message="Invalid value received. {}".format(str(e)), status_code=403)


def app_error_handlers(app: Flask):
    app.register_error_handler(CustomError, lambda e: __error_response(message=e.message, status_code=e.status_code))
    app.register_error_handler(SQLAlchemyError, __db_errors)
    app.register_error_handler(OperationalError, __db_errors)
    app.register_error_handler(TypeError, __handle_type_errors)
    app.register_error_handler(Exception, __unhandled_errors)
