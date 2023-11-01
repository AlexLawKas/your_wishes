from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from wishes.models import Wishes


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishes
        fields = '__all__'
        read_only_fields = ('created_by',)
