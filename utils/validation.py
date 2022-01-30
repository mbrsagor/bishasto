def password_validation(attrs):
    if len(attrs.get('password')) <= 8:
        return "The password should be at-lest 8 charters"
    else:
        pass
