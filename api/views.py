from rest_framework.generics import ListAPIView, RetrieveAPIView 

from .serializers import CompanyDetailSerializer, CompanyListSerializer
from .models import Company


class CompanyListView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer


class CompanyRetriveView(RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'ric_code'

