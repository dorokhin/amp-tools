import unittest
from unittest import mock
from amp_tools import TransformHtmlToAmp
from amp_tools.tests.utils import mocked_requests_get


class TestTransformHtmlToAmp(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTransformHtmlToAmp, self).__init__(*args, **kwargs)
        self.domain = 'dorokhin.moscow'
        self.protocol = 'https://'
        self.image_url = 'https://dorokhin.moscow/media/test.png'

    def test_construct_url_return_passed_valid_url(self):
        full_url = self.protocol + self.domain
        self.assertEqual(TransformHtmlToAmp.construct_url(full_url, self.protocol), full_url)

    def test_construct_url_return_valid_url_when_no_url_prefix(self):
        full_url = self.protocol + self.domain
        self.assertEqual(TransformHtmlToAmp.construct_url(self.domain, self.protocol), full_url)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_image_size(self, mock_get):
        width, height = TransformHtmlToAmp.get_image_size(self.image_url)
        self.assertEqual(width, 200)
        self.assertEqual(height, 50)


if __name__ == '__main__':
    unittest.main()
