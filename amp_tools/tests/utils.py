from io import BytesIO
from PIL import Image


def create_test_image():
    file = BytesIO()
    image = Image.new('RGBA', size=(200, 50), color=(0, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.content = create_test_image().read()

        def json(self):
            return self.json_data

    if args[0] == 'https://dorokhin.moscow/media/test.png':
        return MockResponse({"key1": "value1"}, 200)

    return MockResponse(None, 404)
