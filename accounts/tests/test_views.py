"""
Unit tests for views in auth module
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

import configurations
configurations.setup()
User = get_user_model()

class AdminPageTest(TestCase):
    """
    Unit tests for admin page
    """

    def setUp(self):
        User.objects.create(username='admin')

    def tearDown(self):
        user = get_user_model()
        user.objects.filter(username='admin').delete()
