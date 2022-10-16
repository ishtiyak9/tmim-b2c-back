from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
import jwt
from rest_framework import permissions
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from user.serializers import *
from user.models import *
from vendorprofile.models import *
from vendorprofile.serializers import VendorProfileSerializer
from user.token import account_activation_token


def index(request):
    return render(request, 'index.html', {})


# Create your views here.
class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # if user.user_type == 'vendor':
            #     subscription_plan_info = Subscription.objects.filter(vendor_id=user.id)
            #     print("subscription_plan_info=>", subscription_plan_info)
            #     response = {
            #         # 'success': 'True',
            #         # 'status code': status.HTTP_200_OK,
            #         'subscription': 0,
            #         'group': serializer.data['group'],
            #         'token': serializer.data['token'],
            #         # 'exp': serializer.data['token'],
            #     }
            # else:
            response = {
                # 'success': 'True',
                # 'status code': status.HTTP_200_OK,
                # 'message': 'User logged in  successfully',
                'group': serializer.data['group'],
                'token': serializer.data['token'],
                # 'exp': serializer.data
                # 'exp': serializer.data['token'],
            }
            status_code = status.HTTP_200_OK

            return Response(response, status=status_code)

        error_key = list(serializer.errors.keys())[0]
        response = {
            'error': serializer.errors[error_key][0]
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccount(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            response = {
                # 'success': 'True',
                # 'status code': status.HTTP_201_CREATED,
                'message': 'Account is activated now',
                # 'data': []
            }
            return Response(response, status=status.HTTP_201_CREATED)

        else:
            response = {
                # 'success': 'False',
                # 'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Activation token is not valid',
                # 'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CustomerRegistrationView(APIView):
    serializer_class = CustomerRegistratioinSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        request.data['user_type'] = 'Customer'
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            # 'success': 'True',
            # 'status code': status.HTTP_201_CREATED,
            'message': 'Customer registered successfully',
            # 'data': []
        }

        return Response(response, status=status.HTTP_201_CREATED)


class VendorRegistrationView(CreateAPIView):
    serializer_class = VendorRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        company = request.data.pop('company', None)
        # business_category = request.data.pop('business_category', None)
        #
        # try:
        #     get_business_category = BusinessCategory.objects.get(id=business_category)
        # except:
        #     response = {
        #         # 'sucdess': 'False',
        #         # 'status code': status.HTTP_400_BAD_REQUEST,
        #         'message': 'Business category not found',
        #         # 'data': []
        #     }
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

        request.data['user_type'] = 'Vendor'
        request.data['is_active'] = True
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        vendor_profile_data = {
            'user': serializer.data['id'],
            'business_category': 1,
            'company': company
        }
        vendor_profile_serializer = VendorProfileSerializer(data=vendor_profile_data)
        vendor_profile_serializer.is_valid(raise_exception=True)
        vendor_profile_serializer.save()

        response = {
            # 'success':  'True',
            # 'status code': status.HTTP_201_CREATED,
            'message': 'Vendor registered successfully',
            # 'data': []
        }

        return Response(response, status=status.HTTP_201_CREATED)


class CustomerAccountView(APIView):
    serializer_class = CustomerAccountSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = self.serializer_class(user)
        group = str(Group.objects.get(user=request.user))

        if group == 'customer':
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'Customer profile details',
                'data': serializer.data
            }

            return Response(response)

        response = {
            # 'status code': status.HTTP_403_FORBIDDEN,
            'message': 'You are not allowed to view this information',
            # 'data': []
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        group = str(Group.objects.get(user=request.user))

        response = {}
        if serializer.is_valid() and group == 'customer':
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
            }
            serializer.save()
            response['data'] = serializer.data
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        response['success code'] = status.HTTP_400_BAD_REQUEST
        response['message'] = 'Something went wrong'
        response['data'] = serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class VendorAccountView(APIView):
    serializer_class = VendorAccountSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = self.serializer_class(user)
        group = str(Group.objects.get(user=request.user))

        print("request==>", request)
        if group == 'vendor':
            # response = {
            #     'success': 'True',
            #     'status code': status.HTTP_200_OK,
            #     'message': 'Vendor account details',
            #     'data': serializer.data 
            # }

            return Response(serializer.data, status=status.HTTP_200_OK)

        response = {
            # 'status code': status.HTTP_403_FORBIDDEN,
            'message': 'You are not allowed to view this information',
            # 'data': []
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        group = str(Group.objects.get(user=request.user))

        response = {}

        if serializer.is_valid() and group == 'vendor':
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
            }
            serializer.save()
            response['data'] = serializer.data
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        response['success code'] = status.HTTP_400_BAD_REQUEST
        response['message'] = 'Something went wrong'
        response['data'] = serializer.errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()

            response = {
                # 'status': 'success',
                # 'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                # 'data': []
            }

            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
