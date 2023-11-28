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
            raise ValueError("Failed to retreive assistant") from e


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
        client = OpenAI()

        try:
            client = OpenAI()
            return client.beta.assistants.delete(self.__id)
        except Exception as e:
            raise ValueError("Failed to delete thread") from e


    
        
    def create_assistant_file(self, file_id: str) -> 'AssistantFile':
        client = OpenAI()

        try:
            assistant_file = client.beta.assistants.files.create(
                assistant_id=self.__id, 
                file_id=file_id
                )
            return AssistantFile(**assistant_file)
        except Exception as e:
            raise ValueError("Failed to create assistant file") from e