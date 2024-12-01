from api.guardians.types_guardians import TGuardian

fields = list(TGuardian.__annotations__.keys())
private_fields = ('tag', 'date_of_birth', 'phone_number', 'home_address', 'email', 'tier')
