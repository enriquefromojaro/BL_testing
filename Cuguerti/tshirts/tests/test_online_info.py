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

@mock.patch('requests.get')
class GetOnlineInfoTestCase(TestCase):

    # @mock.patch('requests.get', return_value=MockedResponse(200, 'fakey_shirt'))
    def test_static_get_online_info_ok(self, shirt_mock):
        shirt_mock.return_value = MockedResponse(200, 'fakey_shirt')
        # Asking for information
        info = OnlineInformation.get_online_info('fake-site/fakey_shirt')

        # Asserting information is the asked
        self.assertEquals(info, 'fakey_shirt')

    # @mock.patch('requests.get', return_value=MockedResponse(200, LONG_STR_TEST))
    def test_static_get_online_info_substring(self, shirt_mock):

        shirt_mock.return_value = MockedResponse(200, LONG_STR_TEST)

        # Asking for information
        info = OnlineInformation.get_online_info('fake-site/fakey_shirt')

        # we expect the 50 first chars
        expected = LONG_STR_TEST[:50]

        # Asserting information is the asked
        self.assertEquals(info, expected)

    # @mock.patch.object(requests, 'get', return_value=MockedResponse(200, 'fakey_shirt'))
    def test_static_get_online_info_ok_obj_patch(self, shirt_mock):

        shirt_mock.return_value = MockedResponse(200, 'fakey_shirt')

        # Asking for information
        info = OnlineInformation.get_online_info('fake-site/fakey_shirt')

        # Asserting information is the asked
        self.assertEquals(info, 'fakey_shirt')

    # @mock.patch('requests.get', return_value=MockedResponse(404, 'the_shirt_is_a_lie'))
    def test_static_get_online_info_bad_response_ko(self, shirt_mock):

        shirt_mock.return_value = MockedResponse(404, 'the_shirt_is_a_lie')

        msg_regexp = r'^Invalid response\. Status: [1-5]\d{2}$'
        with self.assertRaisesRegexp(ValueError, msg_regexp):
            # Asking for information
            info = OnlineInformation.get_online_info('fake-site/the_shirt_is_a_lie')
            # we can do more things here and it will assert in some point of
            # the whole context it raises te desired exception

    # @mock.patch('requests.get',return_value=MockedResponse(400, 'the_shirt_is_a_lie'))
    def test_static_get_online_info_bad_response_ko_2(self, shirt_mock):

        shirt_mock.return_value = MockedResponse(400, 'the_shirt_is_a_lie')
        msg_regexp = r'^Invalid response\. Status: [1-5]\d{2}$'

        # Asserts that when the callable_obj is called with the args raises the
        # exception
        self.assertRaisesRegexp(
            ValueError,
            msg_regexp,
            OnlineInformation.get_online_info,  # callable_obj
            *('fake-site/the_shirt_is_a_lie',)  # args for the call
        )


class OnlineInfoTestCase(TestCase):

    def test_method_get_info_mocked_static_method(self):

        info = None

        # Creating context in which mock a static method
        with mock.patch.object(OnlineInformation, 'get_online_info') as static_mock:

            # Defining the mock action
            static_mock.return_value = 'fake-shirt'

            # Calling tested method
            info_obj = OnlineInformation('fake-shirt')
            info = info_obj.get_info()

            # Asserting stuff about the call to the static method

            # Asserting the static method has been called exactly 1 time
            self.assertEquals(1, static_mock.call_count)

            # Asserting that the used url is the correct one
            self.assertTupleEqual(
                static_mock.call_args[0],
                ('https://www.qwertee.com/product/fake-shirt',)
            )

            # Asserting there was no kwargs
            self.assertDictEqual(static_mock.call_args[1], {})

        self.assertEquals(info, 'fake-shirt')

    @mock.patch.object(OnlineInformation, 'get_online_info', return_value='fake-shirt')
    @mock.patch.object(OnlineInformation, 'url', new_callable=mock.PropertyMock())
    def test_method_get_info_mocked_property(self, url_mock, static_mock):

        url_mock.return_value = 'http://fake-host/fake-shirt'

        info_obj = OnlineInformation('fake-shirt')
        info = info_obj.get_info()

        self.assertEquals(info, 'fake-shirt')


    @mock.patch.multiple(
        OnlineInformation,
        get_online_info=mock.MagicMock(return_value='fake-shirt'),
        url=mock.PropertyMock(return_value='http://fake-host/fake-shirt')
    )
    def test_method_get_info_mocked_property_multiple(self):

        info_obj = OnlineInformation('fake-shirt')
        info = info_obj.get_info()

        self.assertEquals(info, 'fake-shirt')


class OnlineInfoIntegrationTestCase(TestCase):
    pass
