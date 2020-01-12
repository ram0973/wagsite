"""
Functional tests for auth module
"""
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase

import configurations
configurations.setup()

class HomePageTestCase(LiveServerTestCase):
    """
    Functional tests for admin page
    """
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = get_user_model()
        user.objects.create(email='admin@test.test')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        user = get_user_model()
        user.objects.filter(email='admin@test.test').delete()

    def test_admin_account(self):
        """ Test home page """
        user = get_user_model()
        user.objects.filter(email='admin@test.test')
        assert user.objects.count()
