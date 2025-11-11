from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Lista os campos do modelo que serão expostos na API.
        fields = ['id', 'username', 'email', 'type']