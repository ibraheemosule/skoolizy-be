from marshmallow import pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class BaseSchema(SQLAlchemyAutoSchema):
    @pre_load
    def remove_created_at(self, data, **kwargs):
        if 'created_at' in data:
            del data['created_at']
        return data
