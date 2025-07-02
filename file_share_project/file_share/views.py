from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.urls import reverse
from django.conf import settings
from .serializers import ClientSignupSerializer, FileUploadSerializer,OpsSignupSerializer, EmailTokenObtainPairSerializer
from .utils import generate_signed_token, verify_signed_token
from .permissions import IsOpsUser, IsClientUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from .models import FileUpload
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import FileResponse, Http404

User = get_user_model()

class ClientSignupView(APIView):
    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_signed_token({'user_id': user.id})
            verify_url = request.build_absolute_uri(
                reverse('client-verify-email') + f'?token={token}'
            )
            # Here, you would send the email with verify_url (omitted for now)
            return Response({'verification_url': verify_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OpsSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = OpsSignupSerializer

class ClientVerifyEmailView(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'detail': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        data = verify_signed_token(token, max_age=60*60*24)  # 24 hours expiry
        if not data or 'user_id' not in data:
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=data['user_id'], role='client')
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        if user.is_verified:
            return Response({'detail': 'User already verified.'}, status=status.HTTP_200_OK)
        user.is_verified = True
        user.save()
        return Response({'detail': 'Email verified successfully.'}, status=status.HTTP_200_OK)

class FileUploadView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsOpsUser]

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class ClientFileListView(generics.ListAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated, IsClientUser]

class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]  # Or customize as needed

    def get(self, request, pk):
        try:
            file_obj = FileUpload.objects.get(pk=pk)
        except FileUpload.DoesNotExist:
            raise Http404("File not found.")

        response = FileResponse(file_obj.file.open('rb'), as_attachment=True, filename=file_obj.original_filename)
        return response
