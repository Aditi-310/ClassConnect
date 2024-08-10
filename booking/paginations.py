from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class AdminBookingOrderPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 100
    page_size_query_param = 'page_size'
    
    def get_page_size(self, request):
    # Allow clients to override the page size.
        if self.page_size_query_param:
            try:
                return int(request.query_params[self.page_size_query_param])
            except (KeyError, ValueError):
                pass
        return self.page_size

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'results': data
        })
    
class UserBookingOrderPagination(PageNumberPagination):
    page_size = 9
    page_query_param = 'page'
    max_page_size = 100