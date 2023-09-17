from django.urls import path
from Api.Api_pages.Authentication import LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from Backend.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static 

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),  #? API responsible for the login functionality
    path('refresh_token', TokenRefreshView.as_view(), name='refresh'),  #? API responsible for the refresh functionality
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
