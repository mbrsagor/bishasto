from rest_framework import views, status, permissions
from rest_framework.response import Response

from utils.enum_utils import ROLE
from core.models.item import Item
from utils.validation import validate_item_service
from core.serializers.item_serializer import ItemSerializer
from utils.message import PERMISSION, NOTFOUND, DELETED, NO_CONTENT
from utils.response import prepare_success_response, prepare_error_response, prepare_create_success_response


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
        return Response(prepare_success_response(data), status=status.HTTP_200_OK)

    def post(self, request):
        try:
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
                return Response(prepare_error_response(PERMISSION), status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)


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
                return Response(prepare_error_response(NOTFOUND), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(prepare_error_response(PERMISSION), status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        if serializer is not None:
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        return Response(prepare_error_response(NO_CONTENT), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role == ROLE.ADMIN or request.user.role == ROLE.MANAGER or request.user.role == ROLE.SHOPKEEPER:
            try:
                item = self.get_object(pk)
                if item is not None:
                    item.delete()
                    return Response(prepare_success_response(DELETED), status=status.HTTP_200_OK)
                else:
                    return Response(prepare_error_response(NO_CONTENT), status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                return Response(prepare_error_response(str(ex)), status=status.HTTP_404_NOT_FOUND)
        return Response(prepare_error_response(PERMISSION), status=status.HTTP_401_UNAUTHORIZED)
