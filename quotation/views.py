import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework import permissions

from quotation.serializers import *
from requestforquote.models import *
from requestforquote.serializers import *
from reservation.models import *
from reservation.serializers import *


class QuotationView(APIView):
    serializer_class = QuotationSerializer
    permission_classes = [IsAuthenticated]

    # for single quotation
    def get(self, request, quotation_id, *args, **kwargs):
        user = request.user

        try:
            quotation = Quotation.objects.get(id=quotation_id)
        except:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'No quotation found',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # checking if the rfq of corresponding quotation is included current user or not
        rfq = RFQ.objects.get(id=quotation.rfq.id)
        if user.user_type.lower() == 'vendor':
            vendor = VendorProfile.objects.get(user=user)
        if (user.user_type.lower() == 'vendor' and rfq.vendor != vendor) or (
                user.user_type.lower() == 'customer' and rfq.customer != user):
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'User is not permitted to view this information',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(quotation)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Quotation details',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    # for showing all quotation
    def get(self, request, *args, **kwargs):
        if request.user.user_type.lower() == 'customer':
            quotations = Quotation.objects.filter(customer=request.user)
            print(quotations)
        else:
            vendor = VendorProfile.objects.get(user=request.user)
            quotations = Quotation.objects.filter(vendor=vendor)

        serializer = self.serializer_class(quotations, many=True)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'All quotations of the user',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    # for creating a quotation
    # only vendor can create the quote
    # quotation is created against a rfq
    def post(self, request, rfq_id, *args, **kwargs):
        global result
        user = request.user
        try:
            vendor = VendorProfile.objects.get(user=user)
            # print("Vendor ===>", vendor)
        except:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'User is not permitted to do this action',
                'data': []
            }
            result = Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            rfq = RFQ.objects.get(id=rfq_id)
        except:
            response = {
                'success': False,
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'RFQ not foundX',
                'data': []
            }
            result = Response(response, status=status.HTTP_404_NOT_FOUND)


        # print("=== === ===>", rfq.vendor)
        # if rfq.vendor != vendor:
        #     response = {
        #         'success': False,
        #         'status_code': status.HTTP_400_BAD_REQUEST,
        #         'message': 'RFQ not foundY',
        #         'data': []
        #     }
        #     result = Response(response, status=status.HTTP_400_BAD_REQUEST)

        if rfq.status == 2:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'RFQ is closed',
                'data': []
            }
            result = Response(response, status=status.HTTP_400_BAD_REQUEST)

        """
        check if quotation already exist for the RFQ or not,
        if exist return failed else execute function and return value.
        """
        # try:
        quote = Quotation.objects.filter(rfq=rfq_id)
        # print("Quotation ===> ", len(quote))
        if len(quote) != 0:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Quotation already exist for this RFQ',
                'data': []
            }
            result = Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            a = request.data
            print("===> except print ===> 1", rfq_id)

            request.data['rfq'] = rfq_id
            print("===> except print ===> 2")
            request.data['customer'] = rfq.customer.id
            request.data['vendor'] = rfq.vendor.id
            request.data['created_by'] = request.user.id
            request.data['updated_by'] = request.user.id

            # if date, start_time, end_time not in request data then use the rfq information
            request_data_keys = request.data.keys()

            if "date" not in request_data_keys:
                request.data['date'] = rfq.date
            if "start_time" not in request_data_keys:
                request.data['start_time'] = rfq.start_time
            if "end_time" not in request_data_keys:
                request.data['end_time'] = rfq.end_time
            print("===> except print ===> 3")
            serializer = self.serializer_class(data=request.data)
            print("===> except print ===> 4")
            if serializer.is_valid(raise_exception=True):
                print("===> except print ===> 5")
                serializer.save()
                response = {
                    'success': True,
                    'status_code': status.HTTP_201_CREATED,
                    'message': 'Quotation created successfully',
                    'data': serializer.data
                }
                result = Response(response, status=status.HTTP_201_CREATED)
        # except:
        #     response = {
        #         'success': False,
        #         'status_code': status.HTTP_400_BAD_REQUEST,
        #         'message': 'Quoation creation failed',
        #         'data': []
        #     }
        #     result = Response(response, status=status.HTTP_400_BAD_REQUEST)

        return result


class QuotationUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuotationSerializer

    def post(self, request, quotation_id, *args, **kwargs):
        quotation_status = request.data['status']
        user = request.user

        try:
            quotation = Quotation.objects.get(id=quotation_id)

            # check if the quotation is already closed or not
            if quotation.status == 2:
                response = {
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'This quotation is already closed',
                    'data': []
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Quotation not found',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # check if the quotation corresponding rfq contains the same vendor or customer
        rfq = RFQ.objects.get(id=quotation.rfq.id)
        if user.user_type.lower() == 'vendor':
            vendor = VendorProfile.objects.get(user=user)

        if (user.user_type.lower() == 'vendor' and rfq.vendor != vendor) or (
                user.user_type.lower() == 'customer' and rfq.customer != user):
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'User is not allowed to perform this action',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # customer can't set status to 1 or 2
        if (int(quotation_status) == 1 or int(quotation_status) == 2) and (user.user_type.lower() != 'vendor'):
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'User is not allowed to do this action',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # vendor can't set status to 3 or 4
        if (int(quotation_status) == 3 or int(quotation_status) == 4) and (user.user_type.lower() != 'customer'):
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'User is not allowed to perform this action',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # customer is not allowed to edit the information added below
        if request.user.user_type.lower() == 'customer':
            date = request.data.pop('date', None)
            start_time = request.data.pop('start_time', None)
            end_time = request.data.pop('end_time', None)
            price = request.data.pop('price', None)
            attachment = request.data.pop('attachment', None)

        # if quotation is accepted by customer
        # then create the reservation
        if int(quotation_status) == 3:
            # check if reservation already created for the quotation or not
            try:
                reservation = Reservation.objects.get(quotation=quotation.id)
                response = {
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Reservation already created for this quotation',
                    'data': []
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            # if reservation not created then create the reservation
            except:
                reservation_data = {
                    "quotation": quotation.id,
                    "total_amount": quotation.price,
                    "is_approved": False,
                    "reservation_date": quotation.date,
                    "reservation_start_time": quotation.start_time,
                    "reservation_end_time": quotation.end_time,
                    "customer": quotation.customer.id,
                    "vendor": quotation.vendor.id,
                }
                reservation_serializer = ReservationSerializer(data=reservation_data)
                if reservation_serializer.is_valid(raise_exception=True):
                    reservation_serializer.save()
                    # response = {
                    #     'success': True,
                    #     'status_code': status.HTTP_201_CREATED,
                    #     'message': 'Reservation created successfully',
                    #     'data': reservation_serializer.data
                    # }
                    # return Response(response, status=status.HTTP_201_CREATED)

        # if vendor close the quotation
        # corresponding rfq will also close
        if int(quotation_status) == 2:
            # close the rfq too
            rfq = RFQ.objects.get(id=quotation.rfq.id)
            rfq_serializer = RFQSerializer(rfq, data={'status': 2, 'updated_by': request.user.id})
            if rfq_serializer.is_valid(raise_exception=True):
                rfq_serializer.save()

        request.data['updated_by'] = user.id
        serializer = self.serializer_class(quotation, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Quotation updated successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
