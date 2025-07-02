from django.urls import path
from .views import ClientSignupView, ClientVerifyEmailView, FileUploadView,OpsSignupView, EmailTokenObtainPairView, ClientFileListView, FileDownloadView

urlpatterns = [
    path('client/signup/', ClientSignupView.as_view(), name='client-signup'),
    path('ops/signup/', OpsSignupView.as_view(), name='ops-signup'),
    path('client/verify-email/', ClientVerifyEmailView.as_view(), name='client-verify-email'),
    path('login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('ops/upload-file/', FileUploadView.as_view(), name='ops-upload-file'),
    path('client/files/', ClientFileListView.as_view(), name='client-file-list'),
    path('client/files/<int:pk>/download/', FileDownloadView.as_view(), name='client-file-download'),
] 