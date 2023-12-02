import unittest
from unittest.mock import patch, MagicMock
from GPTManager.Thread import Thread, Message, MessageFile
import openai
import os
from dotenv import load_dotenv
load_dotenv()

class TestThread(unittest.TestCase):
    mock_message_data = {
        "id": "test_message_id",
        'role': 'user', 
        'file_ids': [],
        "object": "thread.message",
        "created_at": 123456789,
        "thread_id": "test_thread_id",
        "content": [
            {
                "type": "text",
                "text": {
                    "value": "Hello",
                    "annotations": []
                }
            }
        ],
        "assistant_id": None,
        "run_id": None,
        "metadata": {"key": "value"}
    }

    mock_message_file_data = {
        'id': 'test_file_id', 
        'object': 'thread.message.file', 
        'created_at': 123456789,
        'message_id': 'test_message_id'
    }
    
    def setUp(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.thread = Thread()
    
        
    @patch('GPTManager.Thread.OpenAI')
    def test_create_thread(self, mock_openai):

        mock_thread_data = MagicMock()
        mock_thread_data.id = "test_thread_id"
        mock_thread_data.object = "thread"
        mock_thread_data.created_at = 123456789
        mock_thread_data.metadata = {"key": "value"}

        mock_openai.return_value.beta.threads.create.return_value = mock_thread_data

        thread = Thread()
        self.assertEqual(thread._Thread__id, "test_thread_id")
        self.assertEqual(thread._Thread__object, "thread")
        self.assertEqual(thread._Thread__created_at, 123456789)
        self.assertEqual(thread._Thread__metadata, {"key": "value"})


    @patch('GPTManager.Thread.OpenAI')
    def test_retrieve_thread(self, mock_openai):
        # Mocking the OpenAI client and its response
        mock_thread_data = MagicMock()
        mock_thread_data.id = "test_thread_id"
        mock_thread_data.object = "thread"
        mock_thread_data.created_at = 123456789
        mock_thread_data.metadata = {"key": "value"}

        mock_openai.return_value.beta.threads.retrieve.return_value = mock_thread_data

        # Creating a Thread instance with a mock id and calling retrieve_thread
        thread_id = 'test_thread_id'
        thread = Thread(thread_id)

        # Asserting that the thread properties are set as expected
        self.assertEqual(thread._Thread__id, "test_thread_id")
        self.assertEqual(thread._Thread__object, 'thread')
        self.assertEqual(thread._Thread__created_at, 123456789)
        self.assertEqual(thread._Thread__metadata, {"key": "value"})


    @patch('GPTManager.Thread.OpenAI')
    def test_modify_thread(self, mock_openai):
        # Mocking the OpenAI client and its response for thread update
        mock_thread_data = MagicMock()
        mock_thread_data.id = "test_thread_id"
        mock_thread_data.object = "thread"
        mock_thread_data.created_at = 123456789
        mock_thread_data.metadata = {'test_key': 'test_value'}

        mock_openai.return_value.beta.threads.update.return_value = mock_thread_data

        # Creating a Thread instance and calling modify_thread
        self.thread.modify_thread(metadata={'test_key': 'test_value'})

        # Asserting that the __metadata attribute is updated as expected
        self.assertEqual(self.thread._Thread__metadata, {'test_key': 'test_value'})


    @patch('GPTManager.Thread.OpenAI')
    def test_delete_thread(self, mock_openai):
        # Mocking the OpenAI client's response for thread deletion
        mock_delete_response = MagicMock()
        mock_delete_response.id = "test_thread_id"
        mock_delete_response.object = "thread.deleted"
        mock_delete_response.deleted = True

        mock_openai.return_value.beta.threads.delete.return_value = mock_delete_response

        # Creating a Thread instance and calling delete_thread
        response = self.thread.delete_thread()

        # Asserting that the response matches the expected mock response
        self.assertEqual(response.id, "test_thread_id")
        self.assertEqual(response.object, 'thread.deleted')
        self.assertEqual(response.deleted, True)


    @patch('GPTManager.Thread.OpenAI')
    def test_create_message_with_message_object(self, mock_openai):
        # Mocking the OpenAI client's response for message creation
        mock_message_data = {
            "id": "test_message_id",
            'role': 'user', 
            'file_ids': [],
            "object": "thread.message",
            "created_at": 123456789,
            "thread_id": "test_thread_id",
            "content": [
                {
                    "type": "text",
                    "text": {
                        "value": "Hello",
                        "annotations": []
                    }
                }
            ],
            "assistant_id": None,
            "run_id": None,
            "metadata": {}
        }
        mock_openai.return_value.beta.threads.messages.create.return_value = mock_message_data

        mock_message = MagicMock()
        mock_message.role = 'user'
        mock_message.content = 'Hello'
        mock_message.file_ids = []

        result = self.thread.create_message(message=mock_message)
        self.assertIsInstance(result, Message)
        self.assertEqual(
            result.content, 
            [
                {
                    "type": "text",
                    "text": {
                        "value": "Hello",
                        "annotations": []
                    }
                }
            ]
        )


    @patch('GPTManager.Thread.OpenAI')
    def test_create_message_with_params(self, mock_openai):
        # Mocking the OpenAI client's response for message creation
        mock_openai.return_value.beta.threads.messages.create.return_value = self.mock_message_data

        result = self.thread.create_message(role='user', content='Hello')

        self.assertIsInstance(result, Message)
        self.assertEqual(result.role, 'user')
        self.assertEqual(
            result.content, 
            [
                {
                    "type": "text",
                    "text": {
                        "value": "Hello",
                        "annotations": []
                    }
                }
            ]
        )


    @patch('GPTManager.Thread.OpenAI')
    def test_retrieve_message(self, mock_openai):
        # Mocking the OpenAI client's response for message retrieval
        mock_openai.return_value.beta.threads.messages.retrieve.return_value = self.mock_message_data

        result = self.thread.retrieve_message('test_message_id')

        self.assertIsInstance(result, Message)
        self.assertEqual(result.id, 'test_message_id')
        self.assertEqual(
            result.content, 
            [
                {
                    "type": "text",
                    "text": {
                        "value": "Hello",
                        "annotations": []
                    }
                }
            ]
        )
    
    @patch('GPTManager.Thread.OpenAI')
    def test_modify_message_metadata(self, mock_openai):
        # Mocking the OpenAI client's response for message metadata update
        mock_message_data = self.mock_message_data
        mock_message_data['metadata'] = {"test_key": "test_value"}
        mock_openai.return_value.beta.threads.messages.update.return_value = mock_message_data

        result = self.thread.modify_message_metadata('test_message_id', {'test_key': 'test_value'})

        self.assertIsInstance(result, Message)
        self.assertEqual(result.id, 'test_message_id')
        self.assertEqual(result.metadata, {'test_key': 'test_value'})

    @patch('GPTManager.Thread.OpenAI')
    def test_list_thread_messages(self, mock_openai):
        # Mocking the OpenAI client's response for listing thread messages
        mock_messages_data = [
            {**self.mock_message_data, "id" : "message_1" },
            {**self.mock_message_data, "id" : "message_2" },
        ]
        mock_openai.return_value.beta.threads.messages.list.return_value = mock_messages_data

        result = self.thread.list_thread_messages()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all((message, Message) for message in result))

    @patch('GPTManager.Thread.OpenAI')
    def test_retrieve_message_file(self, mock_openai):
        # Mocking the OpenAI client's response for retrieving a message file
        mock_openai.return_value.beta.threads.messages.files.retrieve.return_value = self.mock_message_file_data

        result = self.thread.retrieve_message_file('test_message_id', 'test_file_id')

        self.assertIsInstance(result, MessageFile)
        self.assertEqual(result.id, 'test_file_id')


    @patch('GPTManager.Thread.OpenAI')
    def test_list_message_files(self, mock_openai):
        # Mocking the OpenAI client's response for listing message files
        mock_message_files_data = [
            {**self.mock_message_file_data, 'id': 'file_1'},
            {**self.mock_message_file_data, 'id': 'file_2'}
        ]
        mock_openai.return_value.beta.threads.messages.files.list.return_value = mock_message_files_data

        result = self.thread.list_message_files('test_message_id')

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(file, MessageFile) for file in result))


if __name__ == '__main__':
    unittest.main()
