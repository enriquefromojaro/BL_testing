from unittest import TestCase

import mock


class MocksTestCase (TestCase):

    def test_method(self):

        class TestClass:
             def method(self, *args):
                 pass

        t = TestClass()
        t.method = mock.MagicMock()

        self.assertIsInstance(t.method, mock.MagicMock)

    def test_return_value(self):

        mock_obj = mock.MagicMock()
        mock_obj.return_value = 'Im a mock'

        # print 'Mock return value: ', mock_obj()

        self.assertEquals(mock_obj(), 'Im a mock')
        self.assertEquals(mock_obj(1, 2, 3, 4), 'Im a mock')

    def test_side_effect_basic(self):

        mock_obj = mock.MagicMock()

        mock_obj.side_effect = lambda *args: args

        self.assertEquals(mock_obj(1, 2, 3), (1, 2, 3))

    def test_mock_attr(self):
        mock_obj = mock.MagicMock()

        # mock_obj.glados is a mock
        self.assertIsInstance(mock_obj.glados, mock.Mock)

        val = "How are you mocking up? Because I'm a potato"
        mock_obj.glados.return_value = val

        self.assertEquals(val, mock_obj.glados())

    def test_non_callable_mock(self):
        mock_obj = mock.NonCallableMock()