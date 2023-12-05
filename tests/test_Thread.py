import unittest
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GPTManager.Thread import Thread, Message_Base, Message, MessageFile

import openai
import os
from dotenv import load_dotenv
load_dotenv()

class TestThread(unittest.TestCase):
    mock_thread_data = MagicMock(
        id = "test_thread_id",
        object = "thread",
        created_at = 123456789,
        metadata = {"key": "value"}
    )

    mock_thread_modify_data = MagicMock(
        id = 'test_thread_id',
        object = 'thread',
        created_at = 123456789,
        metadata = {"test_key": "test_value"}
    )

    mock_delete_response = MagicMock(
        id = 'test_thread_id',
        object = 'thread.deleted',
        deleted = True,
    )

    mock_message_data = MagicMock(
        id= "test_message_id",
        role= 'user', 
        file_ids= [],
        object= "thread.message",
        created_at= 123456789,
        thread_id= "test_thread_id",
        content= [
            {
                "type": "text",
                "text": {
                    "value": "Hello",
                    "annotations": []
                }
            }           
        ],
        assistant_id= None,
        run_id= None,
        metadata= {"key": "value"}
    )

    mock_messages_list_data = MagicMock(
        object = "list",
        data = [
            mock_message_data,
            mock_message_data
        ],
        first_id= "test_message_id",
        last_id= "test_message_id",
        has_more= False
    )

    mock_message_modify_data = MagicMock(
        id= "test_message_id",
        role= "user", 
        file_ids= [],
        object= "thread.message",
        created_at= 123456789,
        thread_id= "test_thread_id",
        content= [
            {
                "type": "text",
                "text": {
                    "value": "Hello",
                    "annotations": []
                }
            }           
        ],
        assistant_id= None,
        run_id= None,
        metadata= {"test_key": "test_value"}
    )

    mock_message_file_data = MagicMock(
        id =  'test_file_id', 
        object = 'thread.message.file', 
        created_at = 123456789,
        message_id = 'test_message_id'
    )

    mock_message_file_list_data = MagicMock(
        object = "list",
        data = [
            mock_message_file_data,
            mock_message_file_data
        ],
        first_id= "test_message_id",
        last_id= "test_message_id",
        has_more= False
    )
    
                    
    @patch('GPTManager.Client.OpenAI')
    def setUp(self, mock_openai):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        mock_openai.return_value.beta.threads.create.return_value = self.mock_thread_data
        mock_openai.return_value.beta.threads.retrieve.return_value = self.mock_thread_data
        mock_openai.return_value.beta.threads.update.return_value = self.mock_thread_modify_data
        mock_openai.return_value.beta.threads.delete.return_value = self.mock_delete_response
        mock_openai.return_value.beta.threads.messages.create.return_value = self.mock_message_data
        mock_openai.return_value.beta.threads.messages.retrieve.return_value = self.mock_message_data
        mock_openai.return_value.beta.threads.messages.update.return_value = self.mock_message_modify_data
        mock_openai.return_value.beta.threads.messages.list.return_value = self.mock_messages_list_data
        mock_openai.return_value.beta.threads.messages.files.retrieve.return_value = self.mock_message_file_data
        mock_openai.return_value.beta.threads.messages.files.list.return_value = self.mock_message_file_list_data

        self.thread = Thread()
    

    @patch('GPTManager.Client.OpenAI')
    def test_create_thread(self, mock_openai):

        thread = Thread()
        self.assertEqual(thread.id, "test_thread_id")
        self.assertEqual(thread.object, "thread")
        self.assertEqual(thread.created_at, 123456789)
        self.assertEqual(thread.metadata, {"key": "value"})


    @patch('GPTManager.Client.OpenAI')
    def test_retrieve_thread(self, mock_openai):
        # Creating a Thread instance with a mock id and calling retrieve_thread
        thread = Thread("test_thread_id")
        # Asserting that the thread properties are set as expected
        self.assertEqual(thread.id, "test_thread_id")
        self.assertEqual(thread.object, "thread")
        self.assertEqual(thread.created_at, 123456789)
        self.assertEqual(thread.metadata, {"key": "value"})


    @patch('GPTManager.Client.OpenAI')
    def test_modify_thread(self, mock_openai):
        self.thread.modify_thread(metadata={'test_key': 'test_value'})
        self.assertEqual(self.thread.metadata, {'test_key': 'test_value'})


    @patch('GPTManager.Client.OpenAI')
    def test_delete_thread(self, mock_openai):
        response = self.thread.delete_thread()

        self.assertEqual(response.id, "test_thread_id")
        self.assertEqual(response.object, 'thread.deleted')
        self.assertEqual(response.deleted, True)


    @patch('GPTManager.Client.OpenAI')
    def test_create_message_with_message_object(self, mock_openai):
        message = Message_Base(
            role = 'user',
            content = 'Hello',
            file_ids = []
        )

        result = self.thread.create_message(message=message)

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


    @patch('GPTManager.Client.OpenAI')
    def test_create_message_with_params(self, mock_openai):
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


    @patch('GPTManager.Client.OpenAI')
    def test_retrieve_message(self, mock_openai):
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
    
    @patch('GPTManager.Client.OpenAI')
    def test_modify_message_metadata(self, mock_openai):
        result = self.thread.modify_message_metadata('test_message_id', {'test_key': 'test_value'})

        self.assertIsInstance(result, Message)
        self.assertEqual(result.id, 'test_message_id')
        self.assertEqual(result.metadata, {'test_key': 'test_value'})

    @patch('GPTManager.Client.OpenAI')
    def test_list_thread_messages(self, mock_openai):
        result = self.thread.list_thread_messages()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all((message, Message) for message in result))

    @patch('GPTManager.Client.OpenAI')
    def test_retrieve_message_file(self, mock_openai):
        result = self.thread.retrieve_message_file('test_message_id', 'test_file_id')

        self.assertIsInstance(result, MessageFile)
        self.assertEqual(result.id, 'test_file_id')


    @patch('GPTManager.Client.OpenAI')
    def test_list_message_files(self, mock_openai):
        

        result = self.thread.list_message_files('test_message_id')

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(file, MessageFile) for file in result))


if __name__ == '__main__':
    unittest.main()
