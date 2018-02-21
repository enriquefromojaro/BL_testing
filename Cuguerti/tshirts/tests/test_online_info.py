from unittest import TestCase
from requests import Response as RequestResponse
import requests

import mock

from tshirts.further_features import OnlineInformation


class MockedResponse(RequestResponse):

    def __init__(self, status, text):
        super(MockedResponse, self).__init__()
        self.status_code = status
        self._content = text


class OnlineInfoTestCase(TestCase):

    @mock.patch('requests.get', return_value=MockedResponse(200, 'fakey_shirt'))
    def test_static_get_online_info_ok(self, shirt_mock):

        # Asking for information
        info = OnlineInformation.get_online_info('fake-site/fakey_shirt')

        # Asserting information is the asked
        self.assertEquals(info, 'fakey_shirt')

    @mock.patch.object(requests, 'get', return_value=MockedResponse(200, 'fakey_shirt'))
    def test_static_get_online_info_ok_obj_patch(self, shirt_mock):
        # Asking for information
        info = OnlineInformation.get_online_info('fake-site/fakey_shirt')

        # Asserting information is the asked
        self.assertEquals(info, 'fakey_shirt')
