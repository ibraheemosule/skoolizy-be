from api.staffs.types_staffs import TStaff

fields = list(TStaff.__annotations__.keys())
private_fields = ('tag', 'date_of_birth', 'phone_number', 'home_address', 'email', 'tier')
