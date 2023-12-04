import unittest
from unittest.mock import patch, MagicMock
from GPTManager.Image import Image  # Replace with your actual module name
import openai
import os
from dotenv import load_dotenv
load_dotenv()


class TestImage(unittest.TestCase):
    mock_image_data = {
        'url': 'http://example.com/image',
        'revised_prompt': 'revised prompt text'
    }

    def setUp(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    @patch('GPTManager.Image.OpenAI')
    def test_create_image(self, mock_openai):
        # Mock response
        mock_openai.return_value.generate.return_value = self.mock_image_data

        image = Image(url='', revised_prompt='')
        image.create_image(model='model_name', prompt='revised prompt text', n=1, size='1024x1024')

        # Assertions
        self.assertEqual(image.url, 'http://example.com/image')
        self.assertEqual(image.revised_prompt, 'revised prompt text')

    # @patch('GPTManager.Image.OpenAI')
    # def test_create_image_edit(self, mock_openai):
    #     # Mock response
    #     mock_openai.return_value.edit.return_value = self.mock_image_data

    #     image = Image(b64_json='', url='', revised_prompt='')
    #     image.create_image_edit(image='path/to/image', mask='path/to/mask', prompt='test prompt', n=1, size='1024x1024')

    #     # Assertions
    #     self.assertEqual(image.b64_json, 'base64_encoded_data')
    #     self.assertEqual(image.url, 'http://example.com/image')
    #     self.assertEqual(image.revised_prompt, 'revised prompt text')

    # @patch('GPTManager.Image.OpenAI')
    # def test_create_image_variation(self, mock_openai):
    #     # Mock response
    #     mock_openai.return_value.create_variation.return_value = self.mock_image_data

    #     image = Image(b64_json='', url='', revised_prompt='')
    #     image.create_image_variation(image='path/to/image', n=1, size='1024x1024')

    #     # Assertions
    #     self.assertEqual(image.b64_json, 'base64_encoded_data')
    #     self.assertEqual(image.url, 'http://example.com/image')
    #     self.assertEqual(image.revised_prompt, 'revised prompt text')


if __name__ == '__main__':
    unittest.main()
