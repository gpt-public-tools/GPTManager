import unittest
from unittest.mock import patch, MagicMock
from GPTManager.Thread import Thread
import openai
import os
from dotenv import load_dotenv
load_dotenv()

class TestThread(unittest.TestCase):
    def setUp(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    @patch('GPTManager.Thread.OpenAI') 
    def test_create_thread(self, mock_openai_client):
        # Setup the mock response from OpenAI client
        mock_thread_data = MagicMock()
        mock_thread_data.id = "test_thread_id"
        mock_thread_data.object = "thread"
        mock_thread_data.created_at = 123456789
        mock_thread_data.metadata = {"key": "value"}

        # Set the mock to return the mock data
        mock_openai_client.beta.threads.create.return_value = mock_thread_data

        # Create a Thread instance and call create_thread
        thread = Thread()

        # Assertions to check if the thread attributes are set correctly
        self.assertEqual(thread._Thread__id, "test_thread_id")
        self.assertEqual(thread._Thread__object, "thread")
        self.assertEqual(thread._Thread__created_at, 123456789)
        self.assertEqual(thread._Thread__metadata, {"key": "value"})

        # Check if OpenAI client's create method was called
        mock_openai_client.beta.threads.create.assert_called_once()



if __name__ == '__main__':
    unittest.main()
