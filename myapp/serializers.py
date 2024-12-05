from rest_framework import serializers
from django.contrib.auth.models import User

from myapp.models import CanHo, ChuSoHuu


class CanHoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanHo
        fields = '__all__'

