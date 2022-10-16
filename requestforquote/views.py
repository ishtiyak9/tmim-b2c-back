from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
import jwt
from rest_framework import permissions

from requestforquote.serializers import *
from vendorprofile.models import *
from reservation.models import *
from user.serializers import CustomerRegistratioinSerializer


class RFQView(APIView):
    serializer_class = RFQSerializer
    permission_classes = [IsAuthenticated]

    # for single quote details
    def get(self, request, rfq_id, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)
        try:
            rfq = RFQ.objects.get(pk=rfq_id)
        except:
            response = {
                'success': 'False',
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Quote not found',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if user.user_type.lower() == 'customer':
            serializer = self.serializer_class(rfq)
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Quote details',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        elif user.user_type.lower() == 'vendor' and rfq.vendor == VendorProfile.objects.get(user=user):
            serializer = self.serializer_class(rfq)
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Quote details',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'success': 'False',
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not allowed to view this information',
                'data': []
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    # for closing an rfq
    def post(self, request, rfq_id, *args, **kwargs):
        # checking if quote exist or not
        # checking if found quote belongs to customer or vendor
        try:
            user = User.objects.get(pk=request.user.id)
            vendor = VendorProfile.objects.get(user=user)
            rfq = RFQ.objects.get(pk=rfq_id)
            # print(quote)
            # print(user.user_type)
            if user.user_type.lower() == 'vendor':
                if rfq.vendor != vendor:
                    raise ValueError
            else:
                response = {
                    'success': False,
                    'status_code': status.HTTP_401_UNAUTHORIZED,
                    'message': 'User unauthorized',
                    'data': []
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except:
            response = {
                'success': 'False',
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Quote not found',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # vendor closed the rfq 
        request.data['updated_by'] = request.user.id
        serializer = self.serializer_class(rfq, data=request.data) 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Quotation closed successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        response = {
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Something went wrong',
            'data': []
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CreateRFQView(APIView):
    serializer_class = RFQSerializer
    permission_classes = [AllowAny]

    def post(self, request, vendor_profile_id, *args, **kwargs):
        try:
            vendor = VendorProfile.objects.get(pk=vendor_profile_id)
        except:
            response = {
                'success': 'False',
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'No vendor found with the id',
                'data': []
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if request.user.id:
            serializer = self.serializer_class(data=request.data,
                                               context={'customer': request.user.id, 'vendor': vendor_profile_id})
        # for unregistered user, register him/her
        else:
            first_name = request.data['name'].split(' ')[0]
            try:
                last_name = request.data['name'].split(' ')[1]
            except:
                return Response({'name': 'Please provide full name seperated with space'},
                                status=status.HTTP_400_BAD_REQUEST)
            email = request.data['email']
            password = '12345678tmmim'
            wedding_date = request.data['date']
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
                'wedding_date': wedding_date,
            }
            customer = CustomerRegistratioinSerializer(data=data)
            if customer.is_valid(raise_exception=True):
                customer.save()
                # send email
                # first_name = validated_data['first_name']
                # email = validated_data['email']

                # send_mail(
                #     'Welcome in Tmmim',
                #     f'Hello {first_name}, welcome in Tmmim. Your default passowrd is {password}',
                #     'haris.dipto@gmail.com',
                #     [email],
                #     fail_silently=False
                # )
                customer = customer.data['id']
                serializer = self.serializer_class(data=request.data,
                                                   context={'customer': customer, 'vendor': vendor_profile_id})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Quote created successfully',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)


class AllRFQView(APIView):
    serializer_class = RFQSerializer
    permission_classes = [IsAuthenticated]

    # for all quotes
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)
        if user.user_type.lower() == 'customer':
            quotations = RFQ.objects.filter(customer=request.user.id)
        else:
            vendor = VendorProfile.objects.get(user=request.user.id)
            quotations = RFQ.objects.filter(vendor=vendor)

        serializer = self.serializer_class(quotations, many=True)

        if request.user.id:
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'All quotations',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)

        response = {
            'success': 'True',
            'status_code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Authentication required',
            'data': []
        }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)
