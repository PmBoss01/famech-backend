from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from mechanics.models import MechanicProfile
from mechanics.serializers import MechanicProfileSerializer
from setup.permissions import IsMechanicRole


class MechanicProfileView(GenericAPIView):
    permission_classes = [IsMechanicRole]
    serializer_class = MechanicProfileSerializer

    def get_object(self):
        try:
            return MechanicProfile.objects.get(user=self.request.user)
        except MechanicProfile.DoesNotExist:
            raise NotFound("Mechanic profile not found.")

    def get(self, request):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
