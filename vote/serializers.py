from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Userprofile,Item

class UserprofileSerializer(serializers.ModelSerializer):
    display_picture = serializers.ImageField(required=True)
    # def create(self, validated_data):
    #     user = Userprofile.objects.create(validated_data['display_picture'])
    #     return user
    class Meta:
        model=Userprofile
        fields=['display_picture']

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8,required=True)
    #display_picture = serializers.ImageField(required=True)
    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'], validated_data['email'],
    #          validated_data['password'])#,validated_data['display_picture'])
    #     return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password']#,'display_picture']

    def get_username(self,obj):
        # Provided the user is logged:
        user_username = self.context['request'].user.username
        # Now do whatever with user_id
        return

class ItemStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=['title','count']
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=['title']

    


