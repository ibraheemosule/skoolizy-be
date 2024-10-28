from flask import jsonify
from typing import Dict


def res(*, data: Dict, status_code=200):
    return jsonify({"data": data}), status_code
