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

    mock_runs_list_data = MagicMock(
        object = "list",
        data = [
            mock_run_data,
            mock_run_data
        ],
        first_id= "test_run_id",
        last_id= "test_run_id",
        has_more= False
    )

    mock_submit_tool_data = MagicMock(
        id = "run_abc123",
        object = "thread.run",
        created_at = 1699075592,
        assistant_id = "asst_abc123",
        thread_id = "thread_abc123",
        status = "queued",
        started_at = 1699075592,
        expires_at = 1699076192,
        cancelled_at =  None,
        failed_at =  None,
        completed_at =  None,
        last_error =  None,
        model = "gpt-4",
        instructions = "You tell the weather.",
        tools = [
            MagicMock(
                type= "function",
                function= MagicMock(
                    name= "get_weather",
                    description = "Determine weather in my location",
                    parameters = MagicMock(
                        type = "object",
                        properties = MagicMock(
                            location = MagicMock(
                                type = "string",
                                description = "The city and state e.g. San Francisco, CA"
                            ),
                            unit= MagicMock(
                                type = "string",
                                enum = [
                                    "c",
                                    "f"
                                ]
                            )
                        ),
                        required= [
                            "location"
                        ]
                    )
                )
            )
        ],
        file_ids = [],
        metadata = {}
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
        mock_openai.return_value.beta.threads.runs.list.return_value = self.mock_runs_list_data
        mock_openai.return_value.beta.threads.runs.submit_tool_outputs.return_value = self.mock_submit_tool_data


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

    @patch('GPTManager.Client.OpenAI')
    def test_list_runs(self, mock_openai):
        # Call the list_runs method
        runs = self._run.list_runs()

        # Assert that the method returns a list of Run objects
        self.assertIsInstance(runs, list)
        self.assertEqual(len(runs), 2)
        self.assertIsInstance(runs[0], Run)
        self.assertIsInstance(runs[1], Run)

        # Assert that each Run object has the correct attributes set
        self.assertEqual(runs[0].id, "test_run_id")
        self.assertEqual(runs[1].id, "test_run_id")



if __name__ == '__main__':
    unittest.main()
