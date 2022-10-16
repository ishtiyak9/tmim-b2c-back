from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework import permissions
import jwt
from guest.serializers import *
from guest.models import *


class OccasionListView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        queryset = OccasionType.objects.all()
        serializer = OccasionSerializer(queryset, many=True)

        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Occasion list',
            'data': serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)


class GuestView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_classe = GuestSerializer
    queryset = Guest.objects.all()

    def get(self, request):
        self.queryset = self.queryset.filter(customer=request.user)
        serializer = self.serializer_classe(self.queryset, many=True)
        group = str(Group.objects.get(user=request.user))

        if group == 'customer':
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'Customer guest list',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)

        response = {
            'status code': status.HTTP_403_FORBIDDEN,
            'message': 'You are not allowed to view this information',
            'data': []
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        group = str(Group.objects.get(user=request.user))
        print("Group:", group)
        response = {}

        if group == 'customer':
            request.data["customer"] = request.user.id
            request.data["created_by"] = request.user.id
            request.data["updated_by"] = request.user.id
            request.data["invitation_date"] = request.user.wedding_date
            serializer = self.serializer_classe(data=request.data)

            if serializer.is_valid():
                response = {
                    'success': 'True',
                    'message': 'Guest created successfully',
                    'status code': status.HTTP_201_CREATED
                }
                serializer.save()
                response['data'] = serializer.data
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            print("else printed ++++")

        response['success code'] = status.HTTP_400_BAD_REQUEST
        response['message'] = 'Customers applicable only'
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        group = str(Group.objects.get(user=request.user))
        guest = Guest.objects.get(pk=pk)

        response = {}
        if group == 'customer' and guest.created_by == request.user:
            request.data["created_by"] = request.user.id
            request.data["updated_by"] = request.user.id
            serializer = self.serializer_classe(guest, data=request.data)
            print(serializer)
            print(serializer.is_valid())
            if serializer.is_valid():
                print("XX Valid XX")
                response = {
                    'success': 'True',
                    'message': 'Guest updated successfully',
                    'status code': status.HTTP_201_CREATED
                }
                serializer.save()
                response['data'] = serializer.data
                return Response(response, status=status.HTTP_201_CREATED)

        response['success code'] = status.HTTP_400_BAD_REQUEST
        response['message'] = 'Something went wrong'
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = str(Group.objects.get(user=request.user))
        guest = Guest.objects.get(pk=pk)

        response = {}

        if group == 'customer' and guest.created_by == request.user:
            guest.delete()
            response = {
                'success': 'True',
                'message': 'Guest deleted successfully',
                'status code': status.HTTP_204_NO_CONTENT
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response['success code'] = status.HTTP_400_BAD_REQUEST
        response['message'] = 'Something went wrong'
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GuestlandingView(APIView):
    permission_classes = [AllowAny, ]
    serializer_classe = GuestlandingSerializer

    def get(self, request, customer_id):
        try:
            guestlanding = Guestlanding.objects.get(host=customer_id)
        except:
            response = {
                'success': 'False',
                'message': 'Guest landing page is not created yet',
                'status code': status.HTTP_404_NOT_FOUND,
                'data': []
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if guestlanding:
            serializer = self.serializer_classe(guestlanding)
            response = {
                'success': 'True',
                'message': 'Guest landing page',
                'status code': status.HTTP_200_OK,
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        response = {
            'success': 'False',
            'message': 'Something went wrong',
            'status code': status.HTTP_400_BAD_REQUEST,
            'data': []
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, customer_id):

        if request.user is None or request.user.id != customer_id:
            response = {
                'success': 'False',
                'message': 'Unauthorized user',
                'status code': status.HTTP_403_FORBIDDEN,
                'data': []
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        request.data['host'] = customer_id
        request.data['created_by'] = request.user.id
        request.data['updated_by'] = request.user.id
        serializer = self.serializer_classe(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': 'True',
                'message': 'Guest landing page created successfully',
                'status code': status.HTTP_201_CREATED,
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, customer_id):
        try:
            guestlanding = Guestlanding.objects.get(host=customer_id)
        except:
            response = {
                'success': 'False',
                'message': 'Guest landing page is not created yet',
                'status code': status.HTTP_404_NOT_FOUND,
                'data': []
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if guestlanding and request.user != None and request.user.id == customer_id:
            request.data['created_by'] = guestlanding.created_by.id
            request.data['updated_by'] = request.user.id
            serializer = self.serializer_classe(guestlanding, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {
                'success': 'True',
                'message': 'Guest landing page updated successfully',
                'status code': status.HTTP_205_RESET_CONTENT,
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_205_RESET_CONTENT)

        response = {
            'success': 'False',
            'message': 'Something went wrong',
            'status code': status.HTTP_400_BAD_REQUEST,
            'data': []
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
