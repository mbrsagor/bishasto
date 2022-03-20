from rest_framework import generics, views, status
from rest_framework.response import Response

from core.models.preference import SiteSetting, Preference
from core.serializers.preference_serializer import SiteSettingSerializer, PreferenceSerializer
from utils.response import prepare_create_success_response, prepare_error_response
from utils.enum import ROLE


class SiteSettingCreateListView(generics.ListCreateAPIView):
    queryset = SiteSetting.objects.filter(is_active=True)
    serializer_class = SiteSettingSerializer


class PreferenceCreateListView(views.APIView):
    serializer_class = PreferenceSerializer

    def put(self, request, pk):
        if request.user.role == ROLE.ADMIN or request.user.role == ROLE.MANAGER:
            try:
                preference = Preference.objects.get(id=pk)
                serializer = PreferenceSerializer(preference, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(site='name')
                    return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
                return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(prepare_error_response(str(e)), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(prepare_error_response('You have no permission'), status=status.HTTP_401_UNAUTHORIZED)
