from rest_framework import viewsets
from .models import NGO
from .serializers import NGOSerializer

class NGOViewSet(viewsets.ModelViewSet):
    queryset = NGO.objects.all()
    serializer_class = NGOSerializer