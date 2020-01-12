"""
Functional tests for blog module
"""
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver

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
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--headless')
        # cls.chrome = webdriver.Chrome(chrome_options=chrome_options)
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('-headless')
        cls.firefox = webdriver.Firefox(options=firefox_options)
        user = get_user_model()
        user.objects.create(email='test@test.test')

    @classmethod
    def tearDownClass(cls):
        # cls.chrome.close()
        cls.firefox.close()
        super().tearDownClass()
        user = get_user_model()
        user.objects.filter(email='test@test.test').delete()

    def test_home(self):
        """ Test home page """
        # self.chrome.get('{}'.format(self.live_server_url))
        # assert 'Home' in self.chrome.page_source
        self.firefox.get('{}'.format(self.live_server_url))
        assert 'Home' in self.firefox.page_source
