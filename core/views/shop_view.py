from rest_framework import views, status, permissions
from rest_framework.response import Response

from core.models.shop import Shop
from utils.message import NOTFOUND, DELETED
from core.serializers.shop_serializer import ShopSerializer
from utils.response import prepare_success_response, prepare_error_response


class ShopProfileAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    Name: Shop/store create listview.
    Desc: Vendor can create shop for selling products/items
    URL: /api/v1/shop/
    Method: POST, GET
    """

    def get(self, request):
        shop = Shop.objects.filter(owner=self.request.user)
        serializer = ShopSerializer(shop, many=True)
        return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        try:
            serializer = ShopSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=self.request.user)
                return Response(prepare_success_response(serializer.data), status=status.HTTP_201_CREATED)
            return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_404_NOT_FOUND)


class ShopProfileUpdateDelete(views.APIView):
    """
    Name: Shop update and delete API
    Desc: Vendor can update and delete thire shop.
    URL: /api/v1/shop/<pk>/
    Method: PUT, DELETE
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Shop.objects.filter(id=pk).first()
        except Shop.DoesNotExist:
            return None

    def put(self, request, pk):
        shop = self.get_object(pk)
        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user)
            return Response(prepare_success_response(serializer.data), status=status.HTTP_201_CREATED)
        return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shop = self.get_object(pk)
        if shop is not None:
            shop.delete()
            return Response(prepare_success_response(DELETED), status=status.HTTP_200_OK)
        else:
            return Response(prepare_error_response(NOTFOUND), status=status.HTTP_400_BAD_REQUEST)
