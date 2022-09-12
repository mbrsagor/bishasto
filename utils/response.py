def prepare_create_success_response(serializer_data):
    """ prepare success response for all serializer """
    response = {
        'type': 'success',
        'message': 'Data Successfully created',
        'data': serializer_data
    }
    return response


def prepare_create_success_auth(message):
    """ prepare success response for all serializer """
    response = {
        'status': True,
        'message': message
    }
    return response


def prepare_auth_failed(message):
    """ prepare success response for all serializer """
    response = {
        'status': False,
        'message': message
    }
    return response



def prepare_success_response(serializer_data):
    """ prepare success response for all serializer """
    response = {
        'type': 'success',
        'message': 'Data successfully returned',
        'data': serializer_data
    }
    return response


def prepare_error_response(serializer_error):
    """ prepare error response for all serializer """
    response = {
        'type': 'error',
        'message': serializer_error,
        "data": None
    }
    return response
