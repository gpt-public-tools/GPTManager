import unittest
from unittest.mock import patch, MagicMock
from GPTManager.Organization import Organization  
import openai
import os
from dotenv import load_dotenv
load_dotenv()


class TestOrganization(unittest.TestCase):
    mock_file_data = {
        'id': 'test_file_id',
        'object' : 'file',
        'bytes': 1000,
        'created_at': 123456789,
        'filename': 'test_file_name',
        'purpose': 'assistants_output'
    }

    mock_assistant_data = {
        'id': 'test_assistant_id',
        'object' : 'assistant',
        'created_at': 123456789,
        "name": "Math Tutor",
        "description": None,
        "model": "gpt-4-1106-preview",
        "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
        "tools": [],
        "file_ids": [],
        "metadata": {}
    }


    def setUp(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')


    @patch('GPTManager.Organization.OpenAI')
    def test_list_files(self, mock_openai):
        mock_files_data = [
            {**self.mock_file_data, 'id': 'file_1' },
            {**self.mock_file_data, 'id': 'file_2'},
        ]

        mock_openai.return_value.files.list.return_value = {'data': mock_files_data}

        # Call method
        result = Organization.list_files()

        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 'file_1')
        self.assertEqual(result[1].id, 'file_2')


    @patch('GPTManager.Organization.OpenAI')
    def test_list_assistants(self, mock_openai):
        # Mock response
        mock_assistants_data = [
            {**self.mock_assistant_data, 'id': 'assistant_1' },
            {**self.mock_assistant_data, 'id': 'assistant_2'},
        ]
        
        mock_openai.return_value.beta.assistants.list.return_value = {'data': mock_assistants_data}

        # Call method
        result = Organization.list_assistants(order='asc', limit='10')
        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]._Assistant__object, 'assistant')
        self.assertEqual(result[1]._Assistant__object, 'assistant')


if __name__ == '__main__':
    unittest.main()
