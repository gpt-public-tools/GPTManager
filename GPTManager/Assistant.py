from openai import OpenAI

from dataclasses import dataclass, field
from typing import Any, Optional


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
        __id (str): Assistant ID.
        __object (str): Object type.
        __created_at (int): Creation date.
        __name (Optional[str]): Assistant name.
        __description (Optional[str]): Assistant description.
        __model (str): Model identifier.
        __instructions (Optional[str]): Assistant instructions.
        __tools (List[Tool]): List of tools associated with the assistant.
        __file_ids (List[Any]): List of file IDs associated with the assistant.
        __metadata (dict[str, Any]): Assistant metadata.

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
    __id: str
    __object: str
    __created_at: int
    __name: Optional[str]
    __description: Optional[str]
    __model: str
    __instructions: Optional[str]
    __tools: list[Tool]
    __file_ids: list[Any] = field(default_factory=list)
    __metadata: dict[str, Any] = field(default_factory=dict)


    def __init__(self, assistant_id: str = None):
        """
        Initializes an Assistant object.

        Parameters:
            assistant_id (str): The ID of the assistant to retrieve. If None, a new assistant will be created.

        Returns:
            None
        """
        if assistant_id is not None:
            self.__id = assistant_id
            self.retrieve_assistant()
        else:
            self.create_assistant()


    def create_assistant(
        self, 
        instructions: str, 
        name: str, 
        model: str,
        tools: list[dict[str, str]] = [], 
    ) -> 'Assistant':
        """
        Creates a new assistant using the OpenAI client and sets the __assistant attribute.

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
        client = OpenAI()

        try:
            
            assistant_data = client.beta.assistants.create(
                instructions=instructions,
                name=name,
                tools=tools,
                model=model,
            )

            self.__id = assistant_data.id
            self.__object = assistant_data.object
            self.__created_at = assistant_data.created_at
            self.__name = assistant_data.name
            self.__description = assistant_data.description
            self.__model = assistant_data.model
            self.__instructions = assistant_data.instructions
            self.__tools = assistant_data.tools
            self.__file_ids = assistant_data.file_ids
            self.__metadata = assistant_data.metadata

        except Exception as e:
            raise ValueError("Failed to create assistant") from e


    def retrieve_assistant(self) -> 'Assistant':
        """
        Retrieves the assistant from id using the OpenAI client and sets the __assistant attribute.
       
         Returns:
            None

        Raises:
            ValueError: If the assistant retrieval fails or returns invalid data.
        """
        client = OpenAI()

        try:
            assistant_data = client.beta.assistants.retrieve(self.__id)

            self.__object = assistant_data.object
            self.__created_at = assistant_data.created_at
            self.__name = assistant_data.name
            self.__description = assistant_data.description
            self.__model = assistant_data.model
            self.__instructions = assistant_data.instructions
            self.__tools = assistant_data.tools
            self.__file_ids = assistant_data.file_ids
            self.__metadata = assistant_data.metadata

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
            client = OpenAI()
            assistant_data = client.beta.assistants.update(
                assistant_id=self.__id,
                instructions=instructions,
                name=name,
                tools=[tool.__dict__ for tool in tools],  # Convert Tool objects to dictionaries
                model=model,
                file_ids=file_ids
            )
            
            self.__object = assistant_data.object
            self.__created_at = assistant_data.created_at
            self.__name = assistant_data.name
            self.__description = assistant_data.description
            self.__model = assistant_data.model
            self.__instructions = assistant_data.instructions
            self.__tools = assistant_data.tools
            self.__file_ids = assistant_data.file_ids
            self.__metadata = assistant_data.metadata

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
        client = OpenAI()

        try:
            client = OpenAI()
            return client.beta.assistants.delete(self.__id)
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
        client = OpenAI()

        try:
            assistant_file = client.beta.assistants.files.create(
                assistant_id=self.__id, 
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
        client = OpenAI()

        try:
            assistant_file = client.beta.assistants.files.retrieve(
                assistant_id=self.__id, 
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
        client = OpenAI()

        try:
            return client.beta.assistants.files.delete(
                assistant_id=self.__id, 
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
        client = OpenAI()

        try:
            assistant_files = client.beta.assistants.files.list(
                assistant_id=self.__id
                )
            return [AssistantFile(**assistant_file) for assistant_file in assistant_files]
        except Exception as e:
            raise ValueError("Failed to list assistant files") from e