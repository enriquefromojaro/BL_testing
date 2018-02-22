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

        # use of side_effect with functions (most common use)

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

    def test_mock_constructor(self):

        # Set all prev stuff in the constructor

        mock_obj = mock.MagicMock(
            side_effect=lambda *args: args,
            attr='attr_value',
            **{'re_val.return_value': 'This must return this value'}
        )

        self.assertEquals(mock_obj(1, 2, 3), (1, 2, 3))

        self.assertIsInstance(mock_obj.re_val, mock.Mock)
        self.assertEquals(mock_obj.re_val(), 'This must return this value')
        self.assertEquals(mock_obj.attr, 'attr_value')

    def test_mock_call_count(self):

        mock_obj = mock.MagicMock(return_value='Pos vale')

        mock_obj()
        mock_obj()

        self.assertEquals(2, mock_obj.call_count)

    def test_mock_called(self):
        mock_obj = mock.MagicMock(return_value='Pos vale')

        mock_obj()

        self.assertEquals(True, mock_obj.called)

    def test_mock_call_args(self):
        mock_obj = mock.MagicMock(return_value='Pos vale')

        mock_obj(1, 2, 3, kwarg='kwarg_value')

        self.assertTupleEqual(
            mock_obj.call_args,
            (
                (1, 2, 3),  # Args
                {'kwarg': 'kwarg_value'}  # kwargs
            )
        )

    def test_assert_mock_called(self):
        mock_obj = mock.MagicMock(return_value='Pos vale')

        mock_obj(1, 2, 3, kwarg='kwarg_value')

        mock_obj.assert_called()

    def test_assert_mock_called_once(self):
        """
        Asserts the mock has been called exactly 1 time
        :return:
        """
        mock_obj = mock.MagicMock(return_value='Pos vale')

        mock_obj(1, 2, 3, kwarg='kwarg_value')

        mock_obj.assert_called_once()

    def test_assert_mock_called_once_with(self):
        """
        Asserts the mock has been called exactly 1 time AND with the expected
        params
        """
        mock_obj = mock.MagicMock(return_value='Pos vale')

        mock_obj(1, 2, 3, kwarg='kwarg_value')

        mock_obj.assert_called_once_with(1, 2, 3, kwarg='kwarg_value')

    def test_mock_autospec(self):

        class TestClass:

            def __init__(self, val):
                self.val = val

            def return_val(self):
                return self.val

        with mock.patch.object(TestClass, 'return_val', autospec=True,
                               side_effect=lambda self: (self, 'Mocked: %s' % self.val)):
            instance = TestClass('random_val')
            self.assertTupleEqual(
                instance.return_val(),
                (instance, 'Mocked: random_val')
            )
