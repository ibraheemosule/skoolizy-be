import os
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

    else:
        return jsonify({"error": "db error", "message": str(e)}), 500


def __unhandled_errors(e):
    print(
        os.getenv('OTP_EXPIRY_TIME_IN_MINUTES'),
        os.getenv('EMAIL'),
        os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES'),
        'unhandle err',
    )
    print(e)
    return __error_response(error_type="server error", message=str(e), status_code=500)


def __handle_type_errors(e: TypeError):
    print(
        os.getenv('OTP_EXPIRY_TIME_IN_MINUTES'),
        os.getenv('EMAIL'),
        os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES'),
        'handle type err',
    )

    print(e)
    return __error_response(message="Invalid value received. {}".format(str(e)), status_code=403)


def __handle_value_errors(e: TypeError):
    print(
        os.getenv('OTP_EXPIRY_TIME_IN_MINUTES'),
        os.getenv('EMAIL'),
        os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES'),
        'handle value err',
    )

    if str(e).find('%Y-%m-%d'):
        return __error_response(message="Invalid date format: expected YYYY-MM-DD", status_code=403)
    return __error_response(message="Invalid value received. {}".format(str(e)), status_code=403)


def app_error_handlers(app: Flask):
    app.register_error_handler(CustomError, lambda e: __error_response(message=e.message, status_code=e.status_code))
    app.register_error_handler(SQLAlchemyError, __db_errors)
    app.register_error_handler(OperationalError, __db_errors)
    app.register_error_handler(TypeError, __handle_type_errors)
    app.register_error_handler(ValueError, __handle_value_errors)
    app.register_error_handler(Exception, __unhandled_errors)
