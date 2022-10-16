from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.parsers import MultiPartParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import permission_classes
from checklist.models import Tasklist
from checklist.serializers import TaskSerializer
from vendorprofile.serializers import *
from user.models import *
from reservation.models import *
from reservation.models import *
from django.db.models import Q, Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class VendorAPIView(ListCreateAPIView):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data)


class VendorProfileView(APIView):
    serializer_class = VendorProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, vendor_id, *args, **kwargs):
        try:
            vendor_profile = VendorProfile.objects.get(pk=vendor_id)
        except:
            serializers.ValidationError("No vendor found")

        serializer = self.serializer_class(vendor_profile)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class VendorProfileUpdateView(APIView):
    serializer_class = VendorProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        # try:
        vendor_profile = VendorProfile.objects.get(user=request.user)
        request.data['user'] = request.user.id
        serializer = self.serializer_class(vendor_profile, data=request.data)
        group = str(Group.objects.get(user=request.user))
        # except:
        #     response = {
        #         'status code': status.HTTP_400_BAD_REQUEST,
        #         'message': 'Something went wrongX',
        #         'data': []
        #     }
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if group == 'vendor' and serializer.is_valid():
            serializer.save()
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        response = {
            'status code': status.HTTP_400_BAD_REQUEST,
            'message': 'Something went wrong',
            'data': []
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class FilterProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        response = {
            'status code': status.HTTP_200_OK,
            'message': 'Filtered list',
            'data': []
        }
        query_params = request.query_params
        conditions = {}
        for qp in query_params:
            if (qp != "date" and qp != "start_time" and qp != "end_time"):
                conditions[qp] = query_params[qp][0]

        # filter vendor based on condition
        vendors = VendorProfile.objects.filter(**conditions)
        # find vendor id based on reservation date and time to exclude
        reserved_vendors = []
        for vendor in vendors:
            reservation_start = Reservation.objects.filter(
                vendor=vendor.id,
                is_approved=True,
                # reservation_date=query_params['date'],
                # reservation_start_time__range=[query_params['start_time'], query_params['end_time']]
            )
            reservation_end = Reservation.objects.filter(
                vendor=vendor.id,
                is_approved=True,
                # reservation_date=query_params['date'],
                # reservation_end_time__range=[query_params['start_time'], query_params['end_time']]
            )
            reservation = reservation_start | reservation_end
            if reservation:
                reserved_vendors.append(vendor.id)

        # exclude the vendors
        vendors = vendors.exclude(pk__in=reserved_vendors)

        serializer = VendorProfileSerializer(vendors, many=True)
        response['data'] = serializer.data

        return Response(response, status=status.HTTP_200_OK)


class FilterVendorCategoryWiseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        # exclude the vendors
        vendors = VendorProfile.objects.filter(business_category=pk)

        serializer = VendorProfileHomePageSerializer(vendors, many=True)

        response = {
            'status code': status.HTTP_200_OK,
            'message': 'Filtered list',
            'data': serializer.data
        }

        return Response(response)


class FilterVendorNameWiseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, query):
        # exclude the vendors
        vendors = VendorProfile.objects.all().filter(
            Q(company__contains=query))

        serializer = VendorProfileHomePageSerializer(vendors, many=True)

        response = {
            'status code': status.HTTP_200_OK,
            'message': 'Filtered list',
            'data': serializer.data
        }

        return Response(response)


class BusinessCategoryList(APIView):
    permission_classes = (AllowAny,)

    # authentication_class = JSONWebTokenAuthentication

    def get(self, request, format=None):
        business_category = BusinessCategory.objects.all()
        business_sub_category = BusinessSubCategory.objects.all()
        BusinessCategorySerializer_serializer = BusinessCategorySerializer(business_category, many=True)
        BusinessSubCategorySerializer_serializer = BusinessSubCategorySerializer(business_sub_category, many=True)
        data = {
            "business_category": BusinessCategorySerializer_serializer.data,
            "business_sub_category": BusinessSubCategorySerializer_serializer.data
        }
        return Response(data)

    def post(self, request, format=None):
        serializer = BusinessCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'success': True,
                'status code': status.HTTP_201_CREATED,
                'message': 'Business category saved successfully',
            }
            return Response(content)
        response = {
            'success': False,
            'status code': status.HTTP_400_BAD_REQUEST,
            'message': 'Business Category Does not Exists'
        }
        return Response(response)


class BusinessCategoryDetails(APIView):
    permission_classes = (AllowAny,)
    authentication_class = JSONWebTokenAuthentication

    def get_object(self, pk):
        try:
            return BusinessCategory.objects.get(pk=pk)
        except BusinessCategory.DoesNotExist:
            response = {
                'success': False,
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Business Category Does not Exist'
            }
            return Response(response)

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = BusinessCategorySerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        business_category = self.get_object(pk)
        serializer = BusinessCategorySerializer(business_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'success': True,
                'status code': status.HTTP_201_CREATED,
                'message': 'Business Category Updated Successfully',
            }
            return Response(content)
        response = {
            'success': False,
            'status code': status.HTTP_400_BAD_REQUEST,
            'message': 'Business Category Does not Exist'
        }
        return Response(response)

    def delete(self, request, pk, format=None):
        business_category = self.get_object(pk)
        try:
            business_category.delete()
            content = {
                'success': True,
                'status code': status.HTTP_201_CREATED,
                'message': 'Business Category Deleted Successfully',
            }
            return Response(content)

        except Exception as e:
            response = {
                'success': False,
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Business Category Does not Exist',
            }
            return Response(content)


class ReviewsAndRatingsView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VendorReviewSerializer

    def post(self, request, vendor_id, reservation_id):
        reservation = Reservation.objects.get(pk=reservation_id)

        if reservation.customer == request.user and reservation.vendor.id == vendor_id:
            request.data['customer'] = request.user.id
            request.data['vendor'] = reservation.vendor.id
            request.data['created_by'] = request.user.id
            request.data['updated_by'] = request.user.id
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    'success': 'True',
                    'status code': status.HTTP_201_CREATED,
                    'message': 'Review posted successfully',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)

        response = {
            'success': 'False',
            'status code': status.HTTP_401_UNAUTHORIZED,
            'message': 'You are not allowed to give a review or ratings',
            'data': []
        }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, review_id):
        try:
            review = ReviewsAndRatings.objects.get(pk=review_id)
        except:
            raise serializers.ValidationError("Review not found")

        if review.customer == request.user:
            request.data['created_by'] = request.user.id
            request.data['updated_by'] = request.user.id
            serializer = self.serializer_class(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    'success': 'True',
                    'status code': status.HTTP_201_CREATED,
                    'message': 'Review updated successfully',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)

        response = {
            'success': 'False',
            'status code': status.HTTP_401_UNAUTHORIZED,
            'message': 'You are not allowed to update this review or ratings',
            'data': []
        }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    # def delete(self, request, review_id):
    #     try:
    #         review = ReviewsAndRatings.objects.get(pk=review_id) 
    #     except:
    #         raise serializers.ValidationError("Review not found")

    #     if review.customer == request.user:
    #         review.delete()

    #         response = {
    #             'success': 'True',
    #             'status code': status.HTTP_204_NO_CONTENT,
    #             'message': 'Review deleted successfully',
    #             'data': []
    #         }
    #         return Response(response, status=status.HTTP_201_CREATED)

    #     response = {
    #         'success': 'False',
    #         'status code': status.HTTP_401_UNAUTHORIZED,
    #         'message': 'You are not allowed to delete this review or ratings',
    #         'data': []
    #     }
    #     return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class CalculateReviewView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, vendor_id):
        reviews = ReviewsAndRatings.objects.filter(vendor=vendor_id)

        ratings = 0
        for r in reviews:
            ratings += r.rating

        if (len(reviews) > 0):
            ratings /= len(reviews)

        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Vendor rating',
            'data': ratings
        }

        return Response(response, status=status.HTTP_200_OK)


class HomePageInformation(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, type, format=None):
        tasklist = Tasklist.objects.all().order_by('-id')[:3]
        taskSerilizer = TaskSerializer(tasklist, many=True)

        vendor_list = VendorProfile.objects.filter(occasion_type=type).order_by('-id')[:5]
        vendorSerializer = VendorProfileHomePageSerializer(vendor_list, many=True)

        data = {'checklist': taskSerilizer.data, 'recommended_vendor': vendorSerializer.data}
        # print(data)
        # serializer = BusinessCategorySerializer(business_category, many=True)
        response = {
            'success': True,
            'status code': status.HTTP_200_OK,
            'message': 'Home page',
            'data': data
        }
        return Response(response)
