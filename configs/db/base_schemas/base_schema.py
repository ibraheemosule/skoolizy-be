from marshmallow import pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class BaseSchema(SQLAlchemyAutoSchema):
    @pre_load
    def remove_internal_field(self, data, **kwargs):
        if 'created_at' in data:
            del data['created_at']
        if 'created_by' in data:
            del data['created_by']
        return data
