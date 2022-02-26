from rest_framework import views, status, permissions
from rest_framework.response import Response
from utils.enum import ROLE

from core.models.item import Item
from core.serializers.item_serializer import ItemSerializer
from utils.response import prepare_success_response, prepare_error_response, prepare_create_success_response
from utils.validation import validate_item_service


class ItemAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        item = Item.objects.all()
        serializer = ItemSerializer(item, many=True)
        return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role == ROLE.ADMIN or request.user.role == ROLE.MANAGER or request.user.role == ROLE.SHOPKEEPER:
            validate_error = validate_item_service(request.data)
            if validate_error is not None:
                return Response(prepare_error_response(validate_error), status=status.HTTP_400_BAD_REQUEST)
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(proprietor=self.request.user.shop_owner)
                return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
            return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(prepare_error_response('You have no permission'), status=status.HTTP_400_BAD_REQUEST)


class ItemUpdateDetailDeleteAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return None

    def put(self, request, pk):
        if request.user.role == ROLE.ADMIN or request.user.role == ROLE.MANAGER or request.user.role == ROLE.SHOPKEEPER:
            validate_error = validate_item_service(request.data)
            if validate_error is not None:
                return Response(prepare_error_response(validate_error), status=status.HTTP_400_BAD_REQUEST)
            item = self.get_object(pk)
            if item is not None:
                serializer = ItemSerializer(item, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
                return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(prepare_error_response("No data found for this ID"), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(prepare_error_response('You have no permission'), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        if serializer is not None:
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        return Response(prepare_error_response("Content Not found"), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role == ROLE.ADMIN or request.user.role == ROLE.MANAGER or request.user.role == ROLE.SHOPKEEPER:
            item = self.get_object(pk)
            if item is not None:
                item.delete()
                return Response(prepare_success_response("Data deleted successfully"), status=status.HTTP_200_OK)
            else:
                return Response(prepare_error_response("Content Not found"), status=status.HTTP_400_BAD_REQUEST)
        return Response(prepare_error_response('You have no permission'), status=status.HTTP_400_BAD_REQUEST)
