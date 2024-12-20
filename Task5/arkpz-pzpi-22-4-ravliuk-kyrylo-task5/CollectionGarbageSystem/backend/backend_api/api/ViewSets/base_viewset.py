from rest_framework import viewsets, status
from rest_framework.response import Response

# A generic view set to handle standard CRUD operations for any model
class GenericViewSet(viewsets.ViewSet):
    queryset = None
    serializer_class = None

    # Helper method to format error messages from serializer validation errors
    def format_error(self, errors):
        error_messages = []
        
        for field, msgs in errors.items():
            if isinstance(msgs, list):
                for msg in msgs:
                    error_messages.append(f"{msg}")
            else:
                error_messages.append(f"{msgs}")
        
        return {"error": error_messages}
    
    # Handle GET request to retrieve a list of resources
    def list(self, request):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # Handle GET request to retrieve a single resource by primary key (pk)
    def retrieve(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        except self.queryset.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
    # Handle PUT request to update an existing resource
    def update(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
    # Handle DELETE request to remove an existing resource
    def destroy(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except self.queryset.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)