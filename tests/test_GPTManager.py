import unittest

from GPTManager import Assistant, Run, Thread
import unittest
from unittest.mock import patch, MagicMock
from Thread import Thread, ThreadObject, MessageObject

class TestThread(unittest.TestCase):
  def setUp(self):
    self.thread = Thread()

  @patch('Thread.OpenAI')
  def test_create_thread(self, mock_openai):
    mock_openai().beta.threads.create.return_value = {
      'id': '1', 'object': 'thread', 'created_at': 123456789, 'metadata': {}
    }
    result = self.thread.create_thread()
    self.assertIsInstance(result, ThreadObject)

  @patch('Thread.OpenAI')
  def test_retrieve_thread(self, mock_openai):
    mock_openai().beta.threads.retrieve.return_value = {
      'id': '1', 'object': 'thread', 'created_at': 123456789, 'metadata': {}
    }
    result = self.thread.retrieve_thread('1')
    self.assertIsInstance(result, ThreadObject)

  # Add more test methods for the other methods in the Thread class

if __name__ == '__main__':
  unittest.main()