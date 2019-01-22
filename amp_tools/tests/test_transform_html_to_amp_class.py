import unittest
from lxml import html
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

    def test_transform_span_to_div_img_to_amp_img(self):
        """
        Test:
        change <span> tag to <div>,
        change <img> tag to <amp-img>
        """
        html_elements = '<span class="test-class"><form class="form-test"></form><img src="media/test.png" ' \
                        'width="300" height="220"></span>'
        html_result = b'<div class="amp-text"><amp-img src="media/test.png" width="300" height="220" ' \
                      b'layout="responsive"></amp-img></div>'
        transformed_tag = TransformHtmlToAmp(html_elements)()
        self.assertEqual(transformed_tag, html_result)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_transform_span_to_div_img_to_amp_img_without_image_dimensions(self, mock_get):
        html_elements = '<span class="test-class"><form class="form-test"></form>' \
                        '<img src="https://dorokhin.moscow/media/test.png"></span>'
        html_result = b'<div class="amp-text"><amp-img src="https://dorokhin.moscow/media/test.png" ' \
                      b'width="200" height="50" layout="responsive"></amp-img></div>'
        transformed_tag = TransformHtmlToAmp(html_elements)()
        self.assertEqual(transformed_tag, html_result)


if __name__ == '__main__':
    unittest.main()
