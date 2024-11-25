from flask import jsonify
from typing import Dict
from sqlalchemy.orm import Query
from marshmallow import Schema


def res(*, data: Dict = None, message: str, status_code=200):
    return jsonify({"message": message, **({"data": data} if data else {})}), status_code


def res_paginated(*, schema: Schema, query: Query, page: int, per_page: int, list_type: str):
    paginate = query.paginate(page=page, per_page=per_page, error_out=False)

    return (
        jsonify(
            {
                "message": f"{list_type} list retrieved succesfully",
                "data": {
                    "list": schema.dump(paginate.items),
                    "page": page,
                    "per_page": per_page,
                    "total_items": paginate.total,
                    "total_pages": paginate.pages,
                },
            }
        ),
        200,
    )
