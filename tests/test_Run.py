import unittest
from unittest.mock import patch, MagicMock
from GPTManager.Run import Run, RunStep
from GPTManager.Thread import Thread
from GPTManager.Assistant import Assistant
import openai
import os
from dotenv import load_dotenv
load_dotenv()

class TestRun(unittest.TestCase):
    mock_run_data = MagicMock(
        id= 'test_run_id',  
        object= 'thread.run',
        created_at= 123456789,
        assistant_id= 'test_assistant_id',
        thread_id= 'test_thread_id',
        status= 'completed',
        started_at= 123456789,
        expires_at= None,
        cancelled_at= None,
        failed_at= None,
        completed_at= 123456789,
        last_error= None,
        model= 'gpt-4-1106-preview',
        instructions= None,
        tools= [],
        file_ids= [],
        metadata= {},
    )
    
    mock_run_modify_data = MagicMock(
        id= 'test_run_id',  
        object= 'thread.run',
        created_at= 123456789,
        assistant_id= 'test_assistant_id',
        thread_id= 'test_thread_id',
        status= 'completed',
        started_at= 123456789,
        expires_at= None,
        cancelled_at= None,
        failed_at= None,
        completed_at= 123456789,
        last_error= None,
        model= 'gpt-4-1106-preview',
        instructions= None,
        tools= [],
        file_ids= [],
        metadata= {"new_key": "new_value"},
    )

    @patch('GPTManager.Client.OpenAI')
    def setUp(self, mock_openai):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.thread = Thread()
        self.assistant = Assistant(
            instructions='You are an assistant', 
            name='test_asistant', 
            model='gpt-4-1106-preview', 
            tools=[]
        )
        self.run_id = 'test_run_id'
        self._run = Run(thread_id=self.thread.id, assistant_id=self.assistant.id)
        
        mock_openai.return_value.beta.threads.runs.create.return_value = self.mock_run_data
        mock_openai.return_value.beta.threads.runs.retrieve.return_value = self.mock_run_data
        mock_openai.return_value.beta.threads.runs.update.return_value = self.mock_run_modify_data
        # mock_openai.return_value.beta.threads.runs.list.return_value = self.mock_runs_data


    # Test for create_run method
    @patch('GPTManager.Client.OpenAI')
    def test_create_run(self, mock_openai):
        test_run = Run(thread_id=self.thread.id, assistant_id=self.assistant.id)

        # Assertions
        self.assertEqual(test_run.id, 'test_run_id')
        self.assertEqual(test_run.status, 'completed')


    # Test for retrieve_run method
    @patch('GPTManager.Client.OpenAI')
    def test_retrieve_run(self, mock_openai):
        self._run.retrieve_run()
        self.assertEqual(self._run.object, 'thread.run')
        self.assertEqual(self._run.status, 'completed')


    @patch('GPTManager.Client.OpenAI')
    def test_modify_run(self, mock_openai):
        self._run.modify_run(metadata={"new_key": "new_value"})
        self.assertEqual(self._run.metadata, {"new_key": "new_value"})

    # @patch('GPTManager.Client.OpenAI')
    # def test_list_runs(self, mock_openai):
    #     # Call the list_runs method
    #     runs = self._run.list_runs()

    #     # Assert that the method returns a list of Run objects
    #     self.assertIsInstance(runs, list)
    #     self.assertEqual(len(runs), 2)
    #     self.assertIsInstance(runs[0], Run)
    #     self.assertIsInstance(runs[1], Run)

    #     # Assert that each Run object has the correct attributes set
    #     self.assertEqual(runs[0].id, "run_1")
    #     self.assertEqual(runs[1].id, "run_2")



if __name__ == '__main__':
    unittest.main()
