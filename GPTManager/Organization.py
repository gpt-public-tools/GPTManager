from openai import OpenAI
from . import File, Assistant
import openai
import os
from dotenv import load_dotenv
load_dotenv()

class Organization:

    @staticmethod
    def list_files():
        """
        Lists all files in the OpenAI API.
        
        Parameters:
            None

        Returns:
            list[File]: A list of File objects.
            
        Raises:
            ValueError: If the file list fails or returns invalid data.
        """
        client = OpenAI()
        openai.api_key = os.getenv('OPENAI_API_KEY')

        try:
            files_response = client.files.list()
            return [File(**file) for file in files_response['data']]
        except:
            raise ValueError("Failed to retrieve files")
    
    @staticmethod
    def list_assistants(order: str, limit: str) -> list['Assistant']:
        """
        Lists all assistants in the OpenAI API.
        
        Parameters:
            order (str): The order in which to list the assistants.
            limit (str): The maximum number of assistants to list.
            
        Returns:
            list[Assistant]: A list of Assistant objects.
            
        Raises:
            ValueError: If the assistant list fails or returns invalid data.
        """
        client = OpenAI()
        openai.api_key = os.getenv('OPENAI_API_KEY')

        try:
            asisstants = client.beta.assistants.list(
                order=order,
                limit=limit,
            )
            return [Assistant(**assistant) for assistant in asisstants['data']]
        except Exception as e:
            raise ValueError("Failed to retrieve thread messages") from e

