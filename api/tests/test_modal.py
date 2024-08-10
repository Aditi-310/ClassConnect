from django.test import TestCase
from api.models import Subject,City,User

class SubjectModal(TestCase):
    
    def test_create_subject(self):
        subject_name = 'EPSTIENT'
        
        subject = Subject.objects.create(subject_name=subject_name)
        
        self.assertEqual(subject.subject_name,subject_name)
        self.assertFalse(subject.isDisabled)
        
class CityModal(TestCase):
    
    def test_create_city(self):
        city_name = 'Vapi'
        city_state = 'Gujarat'
        
        city = City.objects.create(city_name=city_name, city_state=city_state)
        
        self.assertEqual(city.city_name,city_name,msg='it should give city name ')
        self.assertEqual(city.city_state, city_state)
        