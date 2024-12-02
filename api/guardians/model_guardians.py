from sqlalchemy import Enum, String, event, select, Index
from configs.db import db
from configs.db.base_models.user_model import UserModel
from utils.constants import user_titles


class Guardian(UserModel):
    __tablename__ = "guardians"
    __tableargs__ = Index('guardian_idx_tag', "tag")

    # Guardian specific fields
    phone_number = db.Column(String(15), nullable=False, unique=True)
    title = db.Column(
        Enum(*user_titles, name="user_title"),
        nullable=False,
    )


@event.listens_for(Guardian, "before_insert")
def generate_tag(mapper, connection, target):
    """
    Generates a tag based for new Guardian before insert.
    """
    last_id_query = select(db.func.max(Guardian.id))
    last_id = connection.execute(last_id_query).scalar()
    target.tag = f'guardian-{(last_id or 0) + 1}'
