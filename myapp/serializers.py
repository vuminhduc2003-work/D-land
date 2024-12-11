from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from myapp.models import CanHo, CuDan


class CanHoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanHo
        fields = '__all__'

    def validate_ma_can_ho(self, value):
        if CanHo.objects.filter(ma_can_ho=value).exists():
            raise ValidationError('This ma_can_ho already exists')
        return value

class CuDanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuDan
        fields = '__all__'
