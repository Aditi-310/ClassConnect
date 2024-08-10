import django_filters
from payment.models import Payment

class PaymentFilter(django_filters.FilterSet):
    payment_date = django_filters.CharFilter(field_name='payment_date', lookup_expr='icontains')
    class Meta:
        model = Payment
        fields = ['payment_date']