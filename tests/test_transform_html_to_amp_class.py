import unittest
from amp_tools import TransformHtmlToAmp


class TestTransformHtmlToAmp(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTransformHtmlToAmp, self).__init__(*args, **kwargs)
        self.domain = 'dorokhin.moscow'
        self.protocol = 'https://'

    def test_construct_url_return_passed_valid_url(self):
        full_url = self.protocol + self.domain
        self.assertEqual(TransformHtmlToAmp.construct_url(full_url, self.protocol), full_url)

    def test_construct_url_return_valid_url_then_no_url_prefix(self):
        full_url = self.protocol + self.domain
        self.assertEqual(TransformHtmlToAmp.construct_url(self.domain, self.protocol), full_url)


if __name__ == '__main__':
    unittest.main()
