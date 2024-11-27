from sqlalchemy import event, select, Index
from configs.db import db
from configs.db.base_models.user_model import UserModel


class Staff(UserModel):
    __tablename__ = "staffs"
    __tableargs__ = Index('staff_idx_tag', "tag")


@event.listens_for(Staff, "before_insert")
def generate_tag(mapper, connection, target):
    """
    Generates a tag based for new Staff before insert.
    """
    last_id_query = select(db.func.max(Staff.id))
    last_id = connection.execute(last_id_query).scalar()
    target.tag = f'staff-{(last_id or 0) + 1}'
