from django.urls import path, include
from user.views import *
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'user'
urlpatterns = [
                  path('', index, name="homepage"),
                  path('token', UserLoginView.as_view(), name='UserLoginAPIView'),
                  path('customer/register', CustomerRegistrationView.as_view(), name="CustomerRegistration"),
                  path('vendor/register', VendorRegistrationView.as_view(), name="VendorRegistration"),
                  path('customer/account', CustomerAccountView.as_view(), name="CustomerAccountDetails"),
                  path('customer/account/update', CustomerAccountView.as_view(), name="CustomerAccountUpdate"),
                  path('vendor/account', VendorAccountView.as_view(), name="VendorAccountDetails"),
                  path('vendor/account/update', VendorAccountView.as_view(), name="VendorAccuontUpdate"),
                  path('password/change', ChangePasswordView.as_view(), name="ChangePassword"),
                  path('password/reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
                  path('activate/<uidb64>/<token>', ActivateAccount.as_view(), name="ActivateAccount")
              ]
