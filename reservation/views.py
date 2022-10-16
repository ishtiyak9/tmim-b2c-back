from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from dateutil.relativedelta import *
from datetime import datetime, date

from reservation.models import *
from reservation.serializers import *


class ReservationView(APIView):
    permission_classes = [IsAuthenticated]
    serailizer_class = ReservationSerializer

    def get(self, request):
        user = request.user
        if user.user_type.lower() == 'customer':
            reservation = Reservation.objects.filter(customer=user.id)
        else:
            vendor = VendorProfile.objects.get(user=user.id)
            reservation = Reservation.objects.filter(vendor=vendor.id)

        # print(type(reservation[0].vendor))
        serializer = ReservationListSerializer(reservation, many=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'All reservations',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        if user.user_type.lower() == 'vendor':
            vendor = VendorProfile.objects.get(user=user.id)
            request.data['vendor'] = vendor.id
            request.data['created_by'] = user.id

            serializer = self.serailizer_class(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    'success': 'True',
                    'status code': status.HTTP_201_CREATED,
                    'message': 'Reservation created successfully',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)

            response = {
                'success': 'False',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'success': 'False',
            'status code': status.HTTP_401_UNAUTHORIZED,
            'message': 'You are not authorized to perform is action',
            'data': []
        }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class ReservationDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        reservation = Reservation.objects.filter(id=pk)

        # print(type(reservation[0].vendor))
        serializer = ReservationListSerializer(reservation, many=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Reservations Details',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class UpdateReservationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def post(self, request, reservation_id, *args, **kwargs):
        # check if the reservation exist or not
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
        except:
            response = {
                'success': False,
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': "Reservation with the given ID doesn't exist",
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendor = VendorProfile.objects.get(user=request.user)
        except:
            response = {
                'success': False,
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User is not allowed to perform this action',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if reservation.vendor != vendor:
            response = {
                'success': False,
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User is not allowed to perform this action',
                'data': []
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        request.data['updated_by'] = request.user.id
        request.data['total_amount'] = reservation.total_amount
        request.data['vendor'] = vendor.id
        serializer = self.serializer_class(reservation, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'status code': status.HTTP_200_OK,
                'message': 'Reservation updated successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        response = {
            'success': False,
            'status code': status.HTTP_400_BAD_REQUEST,
            'message': 'Something went wrong',
            'data': []
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
