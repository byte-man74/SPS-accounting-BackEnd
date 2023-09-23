from django.urls import path
from Api.Api_pages.Authentication import LoginView
from Api.Api_pages.operations.cashbook import *
from rest_framework_simplejwt.views import TokenRefreshView
from Backend.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static 

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),  #?✅ API responsible for the login functionality
    path('refresh_token', TokenRefreshView.as_view(), name='refresh'),  #✅? API responsible for the refresh functionality
    path ('get_amount_available_operations_account', GetAmountAvailableOperationsAccount.as_view(), name='get_amount available'), #✅ API responsible for gettting amount available operations
    path ('get_cash_and_transfer_record', GetTransactionSevenDaysAgo.as_view(), name='get_cash_and transfer_record_seven_days_ago'), #
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
