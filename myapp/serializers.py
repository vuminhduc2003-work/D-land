from rest_framework import serializers
from django.contrib.auth.models import User

from myapp.models import CanHo, ChuSoHuu, CuDan


class CanHoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanHo
        fields = '__all__'

class CuDanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuDan
        fields = '__all__'

class ChuSoHuuSerializer(serializers.ModelSerializer):
    can_ho = serializers.PrimaryKeyRelatedField(queryset=CanHo.objects.all())  # Tham chiếu đến CanHo bằng ID

    class Meta:
        model = ChuSoHuu
        fields = ['id', 'name', 'can_ho']