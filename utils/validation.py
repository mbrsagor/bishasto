def password_validation(attrs):
    if len(attrs.get('password')) <= 8:
        return "The password should be at-lest 8 charters"
    else:
        pass


def validate_item_service(attrs):
    if 'item_name' in attrs and len(attrs.get('item_name')) == 1:
        return "Item name must be more than 1 charter"
    else:
        pass
