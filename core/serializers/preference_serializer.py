from rest_framework import serializers
from core.models.preference import SiteSetting, Preference


class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        read_only_fields = ('site',)
        fields = [
            'id',
            'site',
            'site_name',
            'copyright',
            'logo',
            'footer_logo',
            'favicon',
            'created_at',
            'updated_at',
        ]
