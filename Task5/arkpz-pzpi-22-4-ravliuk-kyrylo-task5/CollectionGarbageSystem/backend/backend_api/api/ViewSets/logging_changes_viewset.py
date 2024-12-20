from rest_framework.viewsets import ReadOnlyModelViewSet
from ...models import AdminLoggingChanges
from ..serializers import AdminLoggingChangesSerializer

class AdminLoggingChangesViewSet(ReadOnlyModelViewSet):
    queryset = AdminLoggingChanges.objects.all()
    serializer_class = AdminLoggingChangesSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)