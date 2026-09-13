from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from service_requests.models import Job, JobStatus, Request
from service_requests.serializers import RequestSerializer
from service_requests.services import find_nearest_mechanics
from setup.permissions import IsOwnerRole, IsRequestOwner
from users.models import Role


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsOwnerRole()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsOwnerRole(), IsRequestOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.MECHANIC:
            return Request.objects.filter(jobs__mechanic=user).distinct()
        return Request.objects.filter(owner=user)

    def perform_create(self, serializer):
        request_obj = serializer.save(owner=self.request.user)
        mechanics = find_nearest_mechanics(request_obj.latitude, request_obj.longitude)
        Job.objects.bulk_create(
            [
                Job(request=request_obj, mechanic=mechanic.user, status=JobStatus.PENDING)
                for mechanic in mechanics
            ]
        )
