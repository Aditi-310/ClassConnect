import django_filters
from .models import User,Subject

class TurorFilter(django_filters.FilterSet):
    subjects = django_filters.CharFilter(field_name='subjects__subject_name', lookup_expr='icontains')    
    # price = django_filters.CharFilter(field_name='price',lookup_expr='lt')
    price = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    class Meta:
        model = User
        fields = ['subjects__subject_name','price']