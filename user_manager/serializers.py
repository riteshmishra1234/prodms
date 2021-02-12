from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=50)
    contact = serializers.CharField(max_length=10)

    def create(self, validated_data):
        try:
            user = User.objects.create(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                contact=validated_data['contact'],

            )
        except :
            raise serializers.ValidationError({'status':'false','error':'email already exists'})

        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        fields = ('id','first_name', 'last_name', 'email', 'contact','avatar','date_joined','is_active','password')
        model = User


class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    contact = serializers.CharField(max_length=10)

    class Meta:
        fields = ('first_name', 'last_name', 'contact')
        model = User


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
