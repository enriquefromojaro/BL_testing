from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', "first_name", "last_name", 'password', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False
            },

        }