from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework import permissions
import jwt

from checklist.serializers import *
from checklist.models import *


class TaskView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        try:
           task = Tasklist.objects.all()
           serializer = TaskSerializer(task, many=True)
           response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'Task list',
                'data': serializer.data
            }

           return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'status code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not allowed to view this information',
                'data': []
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        try:
            request.data["created_by"] = request.user.id
            request.data["updated_by"] = request.user.id
            serializer = TaskSerializer(data=request.data)
            response = {}

            if serializer.is_valid(raise_exception=True):
                response = {
                    'success': 'True',
                    'message': 'Task created successfully',
                    'status code': status.HTTP_201_CREATED
                }
                serializer.save()
                response['data'] = serializer.data
                return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            response['success code'] = status.HTTP_400_BAD_REQUEST
            response['message'] = 'Something went wrong'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        response = {}

        try:
            task = Tasklist.objects.get(pk=pk)
        except:
            response['success code'] = status.HTTP_400_BAD_REQUEST
            response['message'] = 'Task not found'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        request.data["created_by"] = request.user.id
        request.data["updated_by"] = request.user.id
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid(raise_exception=True):
            response = {
                'success': 'True',
                'message': 'Task updated successfully',
                'status code': status.HTTP_201_CREATED
            }
            serializer.save()
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_201_CREATED)

        response['success code'] = status.HTTP_400_BAD_REQUEST
        response['message'] = 'Something went wrong'
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        response = {}

        try:
            task = Tasklist.objects.get(pk=pk)
            task.delete()
            response = {
                'success': 'True',
                'message': 'Task deleted successfully',
                'status code': status.HTTP_204_NO_CONTENT
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            response['success code'] = status.HTTP_400_BAD_REQUEST
            response['message'] = 'Something went wrong'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CheckView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_classe = CheckSerializer
    queryset = Checklist.objects.all()

    def get(self, request):
        self.queryset = self.queryset.filter(customer=request.user)
        serializer = self.serializer_classe(self.queryset, many=True)
        group = str(Group.objects.get(user=request.user))
        print("group->", group)
        if group == 'customer':
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'Check list',
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
        if group == 'customer':
            request.data["customer"] = request.user.id
            request.data["created_by"] = request.user.id
            request.data["updated_by"] = request.user.id
            many = True if isinstance(request.data, list) else False
            serializer = CheckSerializer(data=request.data, many=many)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

            # request.data["customer"] = request.user.id
            # request.data["created_by"] = request.user.id
            # request.data["updated_by"] = request.user.id
            # serializer = self.serializer_classe(data=request.data)
            #
            # response = {}
            #
            # if serializer.is_valid():
            #     response = {
            #         'success': 'True',
            #         'message': 'Check list created successfully',
            #         'status code': status.HTTP_201_CREATED
            #     }
            #     serializer.save()
            #     response['data'] = serializer.data
            #     return Response(response, status=status.HTTP_201_CREATED)

        # response['success code'] = status.HTTP_400_BAD_REQUEST
        # response['message'] = 'Something went wrong'
        # return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        group = str(Group.objects.get(user=request.user))
        check = Checklist.objects.get(pk=pk)

        response = {}

        if group == 'customer' and check.created_by == request.user:
            request.data["created_by"] = str(request.user.id)
            request.data["updated_by"] = request.user.id
            serializer = self.serializer_classe(check, data=request.data)

            if serializer.is_valid():
                response = {
                    'success': 'True',
                    'message': 'Check list updated successfully',
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
        check = Checklist.objects.get(pk=pk)

        response = {}

        if group == 'customer' and check.created_by == request.user:
            check.delete()
            response = {
                'success': 'True',
                'message': 'Check List deleted successfully',
                'status code': status.HTTP_204_NO_CONTENT
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response['success code'] = status.HTTP_400_BAD_REQUEST
        response['message'] = 'Something went wrong'
        return Response(response, status=status.HTTP_400_BAD_REQUEST)