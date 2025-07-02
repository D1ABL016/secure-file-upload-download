from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import FileUpload
import uuid
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

User = get_user_model()

class ClientSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ('email', 'password', 'role')
        extra_kwargs = {'role': {'default': 'client'}}
        

    def validate_role(self, value):
        if value != 'client':
            raise serializers.ValidationError('Role must be client for this endpoint.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password'],
            role='client',
            is_verified=False
        )
        return user

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'file_type', 'upload_time', 'original_filename']
        read_only_fields = ['file_type', 'upload_time', 'original_filename']

    def validate_file(self, value):
        allowed_extensions = ['pptx', 'docx', 'xlsx']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError('Only pptx, docx, and xlsx files are allowed.')
        return value

    def create(self, validated_data):
        file = validated_data['file']
        ext = file.name.split('.')[-1].lower()
        validated_data['file_type'] = ext
        validated_data['original_filename'] = file.name
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)

class   OpsSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='ops',
            is_verified=False
        )
        return user

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user with this email.')

        data = super().validate({
            'username': user.username,
            'password': password
        })
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def to_internal_value(self, data):
        # Accept email and password fields
        return {
            "email": data.get("email"),
            "password": data.get("password"),
        }
