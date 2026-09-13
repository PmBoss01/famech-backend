from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from service_requests.models import Job, JobStatus
from service_requests.serializers import JobSerializer
from service_requests.services import accept_job, complete_job, decline_job
from setup.permissions import IsJobMechanic, IsMechanicRole


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsMechanicRole]

    def get_queryset(self):
        queryset = Job.objects.filter(mechanic=self.request.user)
        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

    def get_permissions(self):
        if self.action in ("accept", "decline", "complete"):
            return [IsAuthenticated(), IsMechanicRole(), IsJobMechanic()]
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        job = self.get_object()
        if job.status != JobStatus.PENDING:
            return Response({"detail": "Job is no longer pending."}, status=400)
        accept_job(job)
        return Response(self.get_serializer(job).data)

    @action(detail=True, methods=["post"])
    def decline(self, request, pk=None):
        job = self.get_object()
        if job.status != JobStatus.PENDING:
            return Response({"detail": "Job is no longer pending."}, status=400)
        decline_job(job)
        return Response(self.get_serializer(job).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        job = self.get_object()
        if job.status != JobStatus.ACCEPTED:
            return Response({"detail": "Job must be accepted before it can be completed."}, status=400)
        complete_job(job)
        return Response(self.get_serializer(job).data)
