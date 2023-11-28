import unittest
from unittest.mock import patch, MagicMock
from GPTManager.Thread import Thread, Message

class TestThread(unittest.TestCase):
    def setUp(self):
        self.thread = Thread()

    @patch('GPTManager.Thread.OpenAI')
    def test_create_thread(self, mock_openai):
        mock_openai().beta.threads.create.return_value = {
            'id': '1', 'object': 'thread', 'created_at': 123456789, 'metadata': {}
        }
        result = self.thread.create_thread()
        self.assertIsInstance(result, Thread)

    @patch('GPTManager.Thread.OpenAI')
    def test_retrieve_thread(self, mock_openai):
        mock_openai().beta.threads.retrieve.return_value = {
            'id': '1', 'object': 'thread', 'created_at': 123456789, 'metadata': {}
        }
        result = self.thread.retrieve_thread()
        self.assertIsInstance(result, Thread)

    @patch('GPTManager.Thread.OpenAI')
    def test_modify_thread(self, mock_openai):
        mock_openai().beta.threads.update.return_value = {
            'id': '1', 'object': 'thread', 'created_at': 123456789, 'metadata': {}
        }
        metadata = {'key': 'value'}
        result = self.thread.modify_thread(metadata)
        self.assertIsInstance(result, Thread)

    @patch('GPTManager.Thread.OpenAI')
    def test_delete_thread(self, mock_openai):
        mock_openai().beta.threads.delete.return_value = {
            'id': 'thread_abc123',
            'object': 'thread.deleted',
            'deleted': True
        }
        result = self.thread.delete_thread()
        self.assertEqual(result['id'], 'thread_abc123')
        self.assertEqual(result['object'], 'thread.deleted')
        self.assertTrue(result['deleted'])

    @patch('GPTManager.Thread.OpenAI')
    def test_create_message_from_message(self, mock_openai):
        message = Message(thread_id='1', role='user', content='Hello')
        mock_openai().beta.threads.messages.create.return_value = {
            'id': 'message_abc123',
            'object': 'message',
            'role': 'user',
            'content': 'Hello',
            'file_ids': []
        }
        result = self.thread.create_message(message=message)
        self.assertIsInstance(result, Message)

    @patch('GPTManager.Thread.OpenAI')
    def test_create_message_from_params(self, mock_openai):
        role = 'user'
        content = 'Hello'
        file_ids = ['file_1', 'file_2']
        mock_openai().beta.threads.messages.create.return_value = {
            'id': 'message_abc123',
            'object': 'message',
            'role': 'user',
            'content': 'Hello',
            'file_ids': ['file_1', 'file_2']
        }
        result = self.thread.create_message(role=role, content=content, file_ids=file_ids)
        self.assertIsInstance(result, Message)

    @patch('GPTManager.Thread.OpenAI')
    def test_retrieve_message(self, mock_openai):
        message_id = 'message_abc123'
        mock_openai().beta.threads.messages.retrieve.return_value = {
            'id': 'message_abc123',
            'object': 'message',
            'role': 'user',
            'content': 'Hello',
            'file_ids': []
        }
        result = self.thread.retrieve_message(message_id)
        self.assertIsInstance(result, Message)

    @patch('GPTManager.Thread.OpenAI')
    def test_modify_message_metadata(self, mock_openai):
        message_id = 'message_abc123'
        metadata = {'key': 'value'}
        mock_openai().beta.threads.messages.update.return_value = {
            'id': 'message_abc123',
            'object': 'message',
            'role': 'user',
            'content': 'Hello',
            'file_ids': [],
            'metadata': {'key': 'value'}
        }
        result = self.thread.modify_message_metadata(message_id, metadata)
        self.assertIsInstance(result, Message)

    @patch('GPTManager.Thread.OpenAI')
    def test_list_thread_messages(self, mock_openai):
        mock_openai().beta.threads.messages.list.return_value = [
            {
                'id': 'message_abc123',
                'object': 'message',
                'role': 'user',
                'content': 'Hello',
                'file_ids': []
            },
            {
                'id': 'message_def456',
                'object': 'message',
                'role': 'assistant',
                'content': 'Hi',
                'file_ids': []
            }
        ]
        result = self.thread.list_thread_messages()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Message)
        self.assertIsInstance(result[1], Message)

    @patch('GPTManager.Thread.OpenAI')
    def test_retrieve_message_file(self, mock_openai):
        message_id = 'message_abc123'
        file_id = 'file_1'
        mock_openai().beta.threads.messages.retrieve_file.return_value = {
            'id': 'file_1',
            'object': 'file',
            'name': 'example.txt',
            'content': 'This is an example file.'
        }
        result = self.thread.retrieve_message_file(message_id, file_id)
        self.assertIsInstance(result, MessageFile)

if __name__ == '__main__':
    unittest.main()