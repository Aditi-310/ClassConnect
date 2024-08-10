from rest_framework.test import APITestCase
from api.serializers import (UserSerializer)

class UserSerailizerTest(APITestCase):
    def test_user_serializer_valid(self):
        data = {
            'email':'amul4577@gmail.com',
            'first_name':'Amul',
            'last_name':'Pande',
            'contact':'9966554488'
        }
        
        serializer = UserSerializer(data=data,partial=True)
        
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors,{})
        