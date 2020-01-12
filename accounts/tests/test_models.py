"""
Unit tests for models in auth module
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

import configurations
configurations.setup()
User = get_user_model()

class UserModelTest(TestCase):
    """
    Tests user model
    """

    def setUp(self):
        User.objects.create(email='test@test.test')

    def tearDown(self):
        User.objects.filter(email='test@test.test').delete()

    def test_user_model_have_admin_record(self):
        """ Test user model have admin record """
        admin = User.objects.first()
        assert admin.email == 'test@test.test'
