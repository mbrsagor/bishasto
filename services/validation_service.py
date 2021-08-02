def validate_service_data(attrs):
    if "name" in attrs and len(attrs.get("name")) < 1:
        return "name field is required"
    elif "manager" is attrs and len(attrs.get("manager")):
        return "Manager field is required"
    else:
        return "Please provide valid services"
