from flask import Flask, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from configs.db import db


class CustomError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def __error_response(*, error_type="client error", message, status_code, context: str = None):
    return jsonify({"error": error_type, "message": message, "context": context}), status_code


def __db_errors(e: SQLAlchemyError):
    try:
        db.session.rollback()

        if getattr(e, 'orig', None):
            code, msg = e.orig.args

            """Handle duplicate value sent for unique field"""
            if code == 1062:
                start_index = msg.rfind('.') + 1
                end_index = msg.rfind("'")

                error_msg = msg[start_index : start_index + 1].upper() + msg[start_index + 1 : end_index]

                return __error_response(message=f"{error_msg} already exists", status_code=403)

            """Handle field can not be null error"""
            if code == 1048:
                start_index = msg.find("'") + 1
                end_index = msg.rfind("'")

                return __error_response(message=f"{msg[start_index : end_index]} is a required", status_code=403)

        return jsonify({"error": "db error", "message": str(e)}), 500
    except Exception as rollback_exception:
        print(f"Rollback failed: {rollback_exception}")
        return __error_response(
            error_type="server error", message="Internal error occurred during rdb ollback", status_code=500
        )


def __unhandled_errors(e):
    print(e)
    return __error_response(
        error_type="server error",
        message="An internal error occured!",
        context=str(e),
        status_code=500,
    )


def __handle_type_errors(e: TypeError):
    print(e)
    return __error_response(message=f"Invalid value received. {str(e)}", status_code=403)


def __db_marshmallow_validation_error(e: ValidationError):
    err_key = list(e.messages.keys())[0]
    return __error_response(message=f"{err_key} {e.messages[err_key][0]}", status_code=403)


def __handle_value_errors(e: TypeError):
    print(str(e))
    return __error_response(message="Invalid value received. {}".format(str(e)), status_code=403)


def __handle_invalid_method_for_route_error(e):
    return __error_response(message="The HTTP method used is not allowed for the requested URL", status_code=405)


def app_error_handlers(app: Flask):
    app.register_error_handler(CustomError, lambda e: __error_response(message=e.message, status_code=e.status_code))
    app.register_error_handler(SQLAlchemyError, __db_errors)
    app.register_error_handler(ValidationError, __db_marshmallow_validation_error)
    app.register_error_handler(OperationalError, __db_errors)
    app.register_error_handler(TypeError, __handle_type_errors)
    app.register_error_handler(ValueError, __handle_value_errors)
    app.register_error_handler(Exception, __unhandled_errors)
    app.register_error_handler(405, __handle_invalid_method_for_route_error)
