import os
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from flask_testing import LiveServerTestCase
from splinter import Browser
from app import create_app


class BrowserTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(BrowserTestCase, cls).setUpClass()
        cls.browser = Browser('chrome', headless=True)
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(BrowserTestCase, cls).tearDownClass()

    def create_app(self):
        app = create_app()
        app.config.update(LIVESERVER_PORT=5000)
        app.secret_key = os.urandom(24)
        return app

    def test_server_is_up_and_running(self):
        response = urlopen(self.get_server_url())
        assert b'GENOME LINK' in response.read()
        assert response.code == 200

    def test_oauth_success(self):
        self.browser.visit(self.get_server_url())
        self.browser.click_link_by_partial_href('https://genomelink.io/oauth/authorize')
        self.browser.find_by_id('id_login').fill('test-user-1')
        self.browser.find_by_id('id_password').fill('genomelink.io')
        self.browser.find_by_name('submit').click()
        assert self.browser.is_text_present('api-oauth-example-flask')
        assert self.browser.is_text_present('eye-color')
        assert self.browser.is_text_present('beard-thickness')
        assert self.browser.is_text_present('morning-person')
        self.browser.find_by_name('allow').click()
        assert self.browser.is_text_present('Genetic eye color')
        assert self.browser.is_text_present('Beard thickness')
        assert self.browser.is_text_present('Morning person')
