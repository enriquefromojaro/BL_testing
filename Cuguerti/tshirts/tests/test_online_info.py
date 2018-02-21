from copy import copy
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


# str 54 chars long
LONG_STR_TEST = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'


class OnlineInfoTestCase(TestCase):

    @mock.patch('requests.get', return_value=MockedResponse(200, 'fakey_shirt'))
    def test_static_get_online_info_ok(self, shirt_mock):

        # Asking for information
        info = OnlineInformation.get_online_info('fake-site/fakey_shirt')

        # Asserting information is the asked
        self.assertEquals(info, 'fakey_shirt')

    @mock.patch('requests.get', return_value=MockedResponse(200, copy(LONG_STR_TEST)))
    def test_static_get_online_info_substring(self, LONG_STR_TEST):
        # Asking for information
        info = OnlineInformation.get_online_info('fake-site/fakey_shirt')

        # we expect the 50 first chars
        expected = LONG_STR_TEST[:50]

        # Asserting information is the asked
        self.assertEquals(info, expected)

    @mock.patch.object(requests, 'get', return_value=MockedResponse(200, 'fakey_shirt'))
    def test_static_get_online_info_ok_obj_patch(self, shirt_mock):
        # Asking for information
        info = OnlineInformation.get_online_info('fake-site/fakey_shirt')

        # Asserting information is the asked
        self.assertEquals(info, 'fakey_shirt')

    @mock.patch('requests.get', return_value=MockedResponse(404, 'the_shirt_is_a_lie'))
    def test_static_get_online_info_bad_response_ko(self, shirt_mock):

        msg_regexp = r'^Invalid response\. Status: [1-5]\d{2}$'
        with self.assertRaisesRegexp(ValueError, msg_regexp):
            # Asking for information
            info = OnlineInformation.get_online_info('fake-site/the_shirt_is_a_lie')
            # we can do more things here and it will assert in some point of
            # the whole context it raises te desired exception

    @mock.patch('requests.get',
                return_value=MockedResponse(400, 'the_shirt_is_a_lie'))
    def test_static_get_online_info_bad_response_ko(self, shirt_mock):

        msg_regexp = r'^Invalid response\. Status: [1-5]\d{2}$'

        # Asserts that when the callable_obj is called with the args raises the
        # exception
        self.assertRaisesRegexp(
            ValueError,
            msg_regexp,
            OnlineInformation.get_online_info,  # callable_obj
            *('fake-site/the_shirt_is_a_lie',)  # args for the call
        )
