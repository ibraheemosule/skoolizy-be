from sqlalchemy import Enum, event, select, Index
from configs.db import db
from configs.db.base_models.user_model import UserModel
from utils.constants import user_titles


class Staff(UserModel):
    __tablename__ = "staffs"
    __tableargs__ = Index('staff_idx_tag', "tag")

    # Staff specific fields
    title = db.Column(
        Enum(*user_titles, name="user_title"),
        nullable=False,
    )


@event.listens_for(Staff, "before_insert")
def generate_tag(mapper, connection, target):
    """
    Generates a tag based for new Staff before insert.
    """
    last_id_query = select(db.func.max(Staff.id))
    last_id = connection.execute(last_id_query).scalar()
    target.tag = f'staff-{(last_id or 0) + 1}'
