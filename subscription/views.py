from django.shortcuts import render, get_object_or_404
from subscription.serializers import SubscriptionPlanSerializer, SubscriptionSerializer
from subscription.models import SubscriptionPlan, Subscription
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.models import User
from dateutil.relativedelta import *
from datetime import datetime, date
from settings.models import Vat

# default_vat = 0

try:
    default_vat = Vat.objects.get(pk=1)
except:
    default_vat = 0


# @login_required()
class SubcriptionPlanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plan = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(plan, many=True)
        # response = {
        #     'success': 'True',
        #     'status code': status.HTTP_200_OK,
        #     'message': 'Product Details',
        #     'data': serializer.data
        # }
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor = request.user

        subsc = Subscription.objects.filter(vendor=vendor, is_deleted=0).order_by('-id')
        serializer = SubscriptionSerializer(subsc, many=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Subscription History',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class SubscriptionDetailsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        tot_subs = Subscription.objects.filter(seller=pk).count()
        if tot_subs > 1:
            subscription_detail = Subscription.objects.filter(seller=pk).order_by('-id')[0]
        else:
            subscription_detail = Subscription.objects.get(seller=pk)

        serializer = SubscriptionSerializer(subscription_detail)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Subscription Details',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class SubcriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        vendor_id = request.user.id
        User.objects.filter(id=vendor_id).update(is_subscribed=1)
        request.data['vendor'] = request.user.id
        request.data['created_by'] = request.user.id
        request.data['updated_by'] = request.user.id

        # fees = float(request.data.get('fees'))
        # vats = str(default_vat)
        # vat_amm = float(vats)
        # vat_percentage = vat_amm / 100
        # vat_amount = fees*vat_percentage

        # request.data['vat_amount'] = vat_amount

        subscription_plan = request.data.get('subscription_plan')
        subscription_plan_info = SubscriptionPlan.objects.get(id=subscription_plan)
        subcription_plan_type = subscription_plan_info.subscription_plan

        today = date.today()

        if subcription_plan_type == 'h':
            expireDate = today + relativedelta(months=+6)
        elif subcription_plan_type == 'y':
            expireDate = today + relativedelta(years=+1)

        request.data['start_date'] = today
        request.data['end_date'] = expireDate

        serializer = SubscriptionSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # serializer.data.vat_amount = vat_amount
            serializer.save()
            # ***********************
            # need to send email here
            # ***********************
            response = {
                'success': 'True',
                'status code': status.HTTP_201_CREATED,
                'message': 'Subscription completed',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            'success': 'False',
            'status code': status.HTTP_400_BAD_REQUEST,
            'message': 'Subscription failed',
            'data': []
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RenewSubscriptionAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        seller_id = request.data.get('seller')
        User.objects.filter(id=seller_id).update(is_subscribed=1)

        fees = float(request.data.get('fees'))
        vats = str(default_vat)
        vat_amm = float(vats)
        vat_percentage = vat_amm / 100
        vat_amount = fees * vat_percentage

        subscription_plan = request.data.get('subscription_plan')

        subscription_plan_info = SubscriptionPlan.objects.get(id=subscription_plan)
        subcription_plan_type = subscription_plan_info.subscription_plan

        today = datetime.now()

        if subcription_plan_type == 'h':
            expireDate = today + relativedelta(months=+6)
        elif subcription_plan_type == 'y':
            expireDate = today + relativedelta(years=+1)

        request.data['vat_amount'] = vat_amount
        request.data['expire_date'] = expireDate

        serializer = SubscriptionSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.data.vat_amount = vat_amount
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def GetSubscriptionById(self, request, pk):
        try:
            model = Subscription.objects.get(id=pk)
            if model.created_by != request.user:
                return None
            return model
        except Subscription.DoesNotExist:
            return

    def delete(self, request, pk):
        if not self.GetSubscriptionById(request, pk):
            return Response(f'Subcription {pk} is Not Found', status=status.HTTP_404_NOT_FOUND)

        if self.GetSubscriptionById(request, pk):
            Subscription.objects.filter(id=pk).update(is_deleted=1)
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'Subscription Canceled'
            }
            return Response(response)
