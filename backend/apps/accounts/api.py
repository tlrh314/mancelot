from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
from mollie.api.client import Client as MollieClient

from accounts.models import UserModel
from accounts.serializers import UserModelSerializer


class UserModelCreateView(generics.CreateAPIView):
    """ This class handles the POST requests of our rest api. """

    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer



class UserModelDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """ This class handles GET, PUT, PATCH and DELETE requests. """

    model = UserModel
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.none()

    def retrieve(self, request):
        user = get_object_or_404(UserModel, pk=request.user.pk)
        serializer = UserModelSerializer(user)
        return Response(serializer.data)

    def update(self, request):
        print(request.user)

    def partial_update(self, request):
        print(request.user)

    def destroy(self, request):
        print(request.user)
