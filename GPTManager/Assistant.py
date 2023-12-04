from openai import OpenAI

from dataclasses import dataclass, field
from typing import Any, Optional

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GPTManager.Client import Client

@dataclass
class AssistantFile:
    id: str
    object: str
    created_at: int
    assistant_id: str


@dataclass
class Tool:
    type: str

@dataclass
class Assistant:
    """
    Class for managing OpenAI Assistants.

    Attributes:
        id (str): Assistant ID.
        object (str): Object type.
        created_at (int): Creation date.
        name (Optional[str]): Assistant name.
        description (Optional[str]): Assistant description.
        model (str): Model identifier.
        instructions (Optional[str]): Assistant instructions.
        tools (List[Tool]): List of tools associated with the assistant.
        file_ids (List[Any]): List of file IDs associated with the assistant.
        metadata (dict[str, Any]): Assistant metadata.

    Methods:
        __init__(self, assistant_id: str = None)
        create_assistant(self, instructions: str, name: str, model: str, tools: list[dict[str, str]] = []) -> 'Assistant'
        retrieve_assistant(self) -> 'Assistant'
        modify_assistant(self, instructions: str, name: Optional[str], tools: list[Tool], model: str, file_ids: list[Any] = [])
        delete_assistant(self)
        create_assistant_file(self, file_id: str) -> 'AssistantFile'
        retrieve_assistant_file(self, file_id: str) -> 'AssistantFile'
        delete_assistant_file(self, file_id: str) -> dict
        list_assistant_files(self) -> list['AssistantFile']
    """
    id: str
    object: str
    created_at: int
    name: Optional[str]
    description: Optional[str]
    model: str
    instructions: Optional[str]
    tools: list[Tool]
    file_ids: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


    def __init__(self, **kwargs) -> 'Assistant':
        """
        Initializes an Assistant object.

        Parameters:
            kwargs: A dictionary of keyword arguments. This can include:
            - assistant_id (str): The ID of the assistant to retrieve. If None, a new assistant will be created.
            - instructions (str):            
            - instructions (str): Detailed instructions or guidelines that define the assistant's operational framework or role.
            - name (str): The name or identifier for the assistant. Used to label or uniquely identify the assistant instance.
            - model (str): The model identifier specifying the underlying AI or computational model that the assistant will use.
            - tools (list[dict[str, str]]): A list of tools (each represented as a dictionary) that the assistant can utilize. Each tool in the list should have specific attributes or properties defined as key-value pairs.


        Returns:
            None
        """
        if 'assistant_id' in kwargs and kwargs['assistant_id'] is not None:
            self.id = kwargs['assistant_id']
            self.retrieve_assistant()
        elif 'instructions' in kwargs and 'name' in kwargs and 'model' in kwargs:
            tools = kwargs.get('tools', [])
            self.create_assistant(
                instructions=kwargs['instructions'], 
                name=kwargs['name'], 
                model=kwargs['model'], 
                tools=tools
            )
        return None


    def create_assistant(
        self, 
        instructions: str, 
        name: str, 
        model: str,
        tools: list[dict[str, str]] = [], 
    ) -> 'Assistant':
        """
        Creates a new assistant using the OpenAI client and sets the assistant attribute.

        Parameters:
            instructions (str): The instructions for the assistant.
            name (str): The name of the assistant.
            model (str): The model identifier.
            tools (list[dict[str, str]]): The list of tools to be associated with the assistant.

        Returns:
            None

        Raises:
            ValueError: If the assistant creation fails or returns invalid data.
        """
        client = Client.get_instance()

        try:
            assistant_data = client.beta.assistants.create(
                instructions=instructions,
                name=name,
                tools=tools,
                model=model,
            )

            self.id = assistant_data.id
            self.object = assistant_data.object
            self.created_at = assistant_data.created_at
            self.name = assistant_data.name
            self.description = assistant_data.description
            self.model = assistant_data.model
            self.instructions = assistant_data.instructions
            self.tools = assistant_data.tools
            self.file_ids = assistant_data.file_ids
            self.metadata = assistant_data.metadata

        except Exception as e:
            raise ValueError("Failed to create assistant") from e


    def retrieve_assistant(self) -> 'Assistant':
        """
        Retrieves the assistant from id using the OpenAI client and sets the assistant attribute.
       
         Returns:
            None

        Raises:
            ValueError: If the assistant retrieval fails or returns invalid data.
        """
        client = Client.get_instance()

        try:
            assistant_data = client.beta.assistants.retrieve(self.id)

            self.object = assistant_data.object
            self.created_at = assistant_data.created_at
            self.name = assistant_data.name
            self.description = assistant_data.description
            self.model = assistant_data.model
            self.instructions = assistant_data.instructions
            self.tools = assistant_data.tools
            self.file_ids = assistant_data.file_ids
            self.metadata = assistant_data.metadata

        except Exception as e:
            raise ValueError("Failed to retrieve assistant") from e


    def modify_assistant(
        self, 
        instructions: str, 
        name: Optional[str], 
        tools: list[Tool], 
        model: str, 
        file_ids: list[Any] = field(default_factory=list)
    ) -> 'Assistant':
        """
        Modifies the assistant's details.

        Parameters:
            instructions (str): New instructions for the assistant.
            name (Optional[str]): New name of the assistant.
            tools (List[Tool]): List of tools to be associated with the assistant.
            model (str): Model identifier.
            file_ids (List[Any]): List of file IDs associated with the assistant.

        Returns:
            None

        Raises:
            ValueError: If assistant modification fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            assistant_data = client.beta.assistants.update(
                assistant_id=self.id,
                instructions=instructions,
                name=name,
                tools=[tool.__dict__ for tool in tools],  # Convert Tool objects to dictionaries
                model=model,
                file_ids=file_ids
            )
            
            self.object = assistant_data.object
            self.created_at = assistant_data.created_at
            self.name = assistant_data.name
            self.description = assistant_data.description
            self.model = assistant_data.model
            self.instructions = assistant_data.instructions
            self.tools = assistant_data.tools
            self.file_ids = assistant_data.file_ids
            self.metadata = assistant_data.metadata

        except Exception as e:
            raise ValueError("Failed to modify assistant") from e


    def delete_assistant(self):
        """
        Deletes the assistant.

        Returns:
            None

        Raises:
            ValueError: If assistant deletion fails.
        """
        client = Client.get_instance()

        try:
            client = Client.get_instance()
            return client.beta.assistants.delete(self.id)
        except Exception as e:
            raise ValueError("Failed to delete assistant") from e

        
    def create_assistant_file(self, file_id: str) -> 'AssistantFile':
        """
        Creates a new assistant file.

        Parameters:
            file_id (str): The ID of the file.

        Returns:
            AssistantFile: The created assistant file.

        Raises:
            ValueError: If assistant file creation fails.
        """
        client = Client.get_instance()

        try:
            assistant_file = client.beta.assistants.files.create(
                assistant_id=self.id, 
                file_id=file_id
                )
            return AssistantFile(**assistant_file)
        except Exception as e:
            raise ValueError("Failed to create assistant file") from e
        

    def retrieve_assistant_file(self, file_id: str) -> 'AssistantFile':
        """
        Retrieves an assistant file.

        Parameters:
            file_id (str): The ID of the file.

        Returns:
            AssistantFile: The retrieved assistant file.

        Raises:
            ValueError: If assistant file retrieval fails.
        """
        client = Client.get_instance()

        try:
            assistant_file = client.beta.assistants.files.retrieve(
                assistant_id=self.id, 
                file_id=file_id
                )
            return AssistantFile(**assistant_file)
        except Exception as e:
            raise ValueError("Failed to retrieve assistant file") from e
        

    def delete_assistant_file(self, file_id: str) -> dict:
        """
        Deletes an assistant file.

        Parameters:
            file_id (str): The ID of the file.

        Returns:
            dict: The response from the API.

        Raises:
            ValueError: If assistant file deletion fails.
        """
        client = Client.get_instance()

        try:
            return client.beta.assistants.files.delete(
                assistant_id=self.id, 
                file_id=file_id
                )
        except Exception as e:
            raise ValueError("Failed to delete assistant file") from e
        
        
    def list_assistant_files(self) -> list['AssistantFile']:
        """
        Lists all assistant files.

        Returns:
            list[AssistantFile]: The list of assistant files.

        Raises:
            ValueError: If listing assistant files fails.
        """
        client = Client.get_instance()

        try:
            assistant_files = client.beta.assistants.files.list(
                assistant_id=self.id
                )
            return [AssistantFile(**assistant_file) for assistant_file in assistant_files]
        except Exception as e:
            raise ValueError("Failed to list assistant files") from e