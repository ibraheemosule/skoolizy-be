immutable_announcement_fields = ("created_at", "id", "announcement_type", "created_by", "recipient", "reminder")
announcement_types = ("memo", "single_event", "multi_event")


def announcement_permission(user):
    user_group = user.get("group")
    tier = user.get("tier")

    access = {user_group: tier, "general": 5}

    if user_group == "staffs":
        if tier == 2:
            access["students"] = 1
        if tier == 3:
            access["students"] = 2
        if tier == 4:
            access["students"] = 3
        if tier == 5:
            access["students"] = 4
            access["guardians"] = 1

    if user_group == 'students':
        if tier == 4:
            access["staffs"] = 1
        if tier == 5:
            access["staffs"] = 2

    if user_group == "guardians":
        if tier == 2:
            access["students"] = 1
        if tier == 4:
            access["students"] = 2
        if tier == 5:
            access["students"] = 3

    return access


def get_recipients_email(announcement_schema):
    recipients = []
    from api.staffs.model_staffs import Staff
    from api.staffs.schema_staff import StaffSchema
    from api.guardians.model_guardians import Guardian
    from api.guardians.schema_guardian import GuardianSchema
    from configs.db import db

    staff_schema = StaffSchema(many=True, session=db.session)
    guardian_schema = GuardianSchema(many=True, session=db.session)

    if announcement_schema.recipient == "general":
        recipients = (
            list(
                map(
                    lambda arg: arg['email'],
                    [*staff_schema.dump(Staff.query.all()), *guardian_schema.dump(Guardian.query.all())],
                )
            )
            or []
        )

    if announcement_schema.recipient == "staffs":
        recipients = list(
            map(lambda arg: arg['email'], staff_schema.dump(Staff.query.filter_by(group=announcement_schema.recipient)))
            or []
        )

    if announcement_schema.recipient == "guardians":
        recipients = list(
            map(
                lambda arg: arg['email'],
                guardian_schema.dump(Guardian.query.filter_by(group=announcement_schema.recipient)),
            )
            or []
        )

    return recipients
