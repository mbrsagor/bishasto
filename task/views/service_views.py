from rest_framework import views, status
from rest_framework.response import Response

from task.models.service import Service
from task.serializers.service_serializer import ServiceSerializer
from services.validation_service import validate_service_data
from services.custom_response import *


class ServiceAPIView(views.APIView):

    def get_object(self, pk):
        try:
            return Service.objects.filter(id=pk).first()
        except Service.DoesNotExist:
            return None

    def get(self, request):
        service = Service.objects.all()
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        validate_error = validate_service_data(request.data)
        if validate_error is not None:
            return Response(prepare_error_response(validate_error), status=status.HTTP_400_BAD_REQUEST)
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        validate_error = validate_service_data(request.data)
        if validate_error is not None:
            return Response(prepare_error_response(validate_error), status=status.HTTP_400_BAD_REQUEST)
        service = Service.objects.filter(id=pk).first()
        if service is not None:
            serializer = ServiceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
            return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(prepare_error_response("No data found for this ID"), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        service = self.get_object(pk=pk)
        if service is not None:
            service.delete()
            return Response(prepare_success_response("Data deleted successfully"), status=status.HTTP_200_OK)
        else:
            return Response(prepare_error_response("Content Not found"), status=status.HTTP_400_BAD_REQUEST)
