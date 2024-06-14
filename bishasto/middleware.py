from django.shortcuts import HttpResponse


class MyProcessMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(request, *args, **kwargs):
        print('This is process view - before view')
        # Prevent to execute view
        # return HttpResponse('This is before view')

        # Allow to execute view
        return None


class MyExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    # Will be executed when exception is occured
    def process_exception(self, request, exception):
        print('Exception occured')
        msg = exception
        class_name = exception.__class__.__name__
        print('class_name: ', class_name)
        print('msg: ', msg)
        return HttpResponse(msg)


class MyTemplateResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    # Will be executed after template response
    def process_template_response(self, request, response):
        print('Process Template Response From Middleware')
        response.context_data['name'] = 'Bozlur Rosid Sagor'
        return response
