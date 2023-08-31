from rest_framework import views, status, permissions
from rest_framework.response import Response

from core.models.item import Item
from utils import message, response, validation, enum_utils
from core.serializers.item_serializer import ItemSerializer


class ItemAPIView(views.APIView):
    """
    Name: Item/product create list API endpoint.
    Description: The API endpoint shopkeeper or admin, manager will only add projects/items.
    Method: get/post
    Endpoint: /api/v1/item/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = []
        item = Item.objects.all()
        serializer = ItemSerializer(item, many=True)
        products = serializer.data
        for product in products:
            res = {
                'id': product['id'],
                'item_name': product['item_name'],
                'category': product['category']['name'],
                'price': product['price'],
                'discount_price': product['discount_price'],
                'model': product['model'],
                'is_available': product['is_available'],
                'tags': product['tags'],
                'item_type': product['item_type'],
                'item_image': product['item_image'],
                'galley_image2': product['galley_image2'],
                'galley_image3': product['galley_image3'],
                'short_description': product['short_description'],
            }
            data.append(res)
        return Response(response.prepare_success_response(data), status=status.HTTP_200_OK)

    def post(self, request):
        try:
            if request.user.role == enum_utils.ROLE.ADMIN or request.user.role == enum_utils.ROLE.MANAGER or request.user.role == enum_utils.ROLE.SHOPKEEPER:
                validate_error = validation.validate_item_service(request.data)
                if validate_error is not None:
                    return Response(response.prepare_error_response(validate_error), status=status.HTTP_400_BAD_REQUEST)
                serializer = ItemSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(proprietor=self.request.user.shop_owner)
                    return Response(response.prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
                return Response(response.prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response.prepare_error_response(message.PERMISSION), status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(response.prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)


class ItemUpdateDetailDeleteAPIView(views.APIView):
    """
       Name: Item/product `update` `details`, and `delete` API endpoint.
       Description: The API endpoint shopkeeper or admin, manager will only add projects/items.
       Method: get/post
       Endpoints::
            update: /api/v1/item/edit/<pk>/
            Details: /api/v1/item/detail/<pk>/
            Details: /api/v1/item/delete/<pk>/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return None

    def put(self, request, pk):
        if request.user.role == enum_utils.ROLE.ADMIN or request.user.role == enum_utils.ROLE.MANAGER or request.user.role == enum_utils.ROLE.SHOPKEEPER:
            validate_error = validation.validate_item_service(request.data)
            if validate_error is not None:
                return Response(response.prepare_error_response(validate_error), status=status.HTTP_400_BAD_REQUEST)
            item = self.get_object(pk)
            if item is not None:
                serializer = ItemSerializer(item, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(response.prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
                return Response(response.prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response.prepare_error_response(message.NOTFOUND), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response.prepare_error_response(message.PERMISSION), status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        if serializer is not None:
            return Response(response.prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        return Response(response.prepare_error_response(message.NO_CONTENT), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role == enum_utils.ROLE.ADMIN or request.user.role == enum_utils.ROLE.MANAGER or request.user.role == enum_utils.ROLE.SHOPKEEPER:
            try:
                item = self.get_object(pk)
                if item is not None:
                    item.delete()
                    return Response(response.prepare_success_response(message.DELETED), status=status.HTTP_200_OK)
                else:
                    return Response(response.prepare_error_response(message.NO_CONTENT), status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                return Response(response.prepare_error_response(str(ex)), status=status.HTTP_404_NOT_FOUND)
        return Response(response.prepare_error_response(message.PERMISSION), status=status.HTTP_401_UNAUTHORIZED)
