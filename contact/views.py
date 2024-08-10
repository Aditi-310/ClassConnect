from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from contact.serailizers import ContactUsSerializer
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdmin
from contact.models import ContactUs
from contact.paginations import ContactUsPaginations
# Create your views here

class ContactUsCreateView(generics.ListCreateAPIView):
    serializer_class = ContactUsSerializer
    pagination_class = ContactUsPaginations
    queryset = ContactUs.objects.filter(isDeleted=False).all()
    
    def get_permissions(self):
        """
        Override method to allow unauthenticated users to create data and only admin to retrieve data.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdmin()]
        return []
    
    
class ContactRetieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()
    permission_classes = [IsAuthenticated,IsAdmin]

    def delete(self, request,pk ,*args, **kwargs):
        try:
            contact = ContactUs.objects.get(pk=pk)
            contact.isDeleted = True
            contact.save()  
            return Response({'message': 'Contact soft deleted successfully'}, status=200)
        except ContactUs.DoesNotExist:
            return Response({'error': 'Contact does not exist'}, status=404)