from openai import OpenAI

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class Tool:
    type: str

@dataclass
class AssistantObject:
    id: str
    object: str
    created_at: int
    name: Optional[str]
    description: Optional[str]
    model: str
    instructions: Optional[str]
    tools: list[Tool]
    file_ids: list[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class Assistant:
    __assistant: AssistantObject  = None

    def __init__(self, assistant_id: str = None):
        if assistant_id:
            self.retrieve_assistant(assistant_id)
        else:
            self.create_assistant()


    @property
    def assistant(self) -> AssistantObject:
        """Getter for __assistant"""
        return self.__assistant


    @assistant.setter
    def assistant(self, value: AssistantObject):
        """Setter for __assistant"""
        if not isinstance(value, AssistantObject):
            raise ValueError("Value must be an instance of AssistantObject")
        self.__assistant = value


    def create_assistant(
        self, 
        instructions: str = "You are an asistant", 
        name: str = "Asistant", 
        tools: list[Dict[str, str]] = [ 
            {
                "type": "code_interpreter"
            }
        ], 
        model: str = "gpt-4-1106-preview"
    ) -> AssistantObject:
        """
        Creates a new assistant using the OpenAI client and sets the __assistant attribute.
        Returns:
            AssistantObject: An instance representing the newly created assistant.
        Raises:
            ValueError: If the assistant creation fails or returns invalid data.
        """
        try:
            client = OpenAI()
            assistant_data = client.beta.assistants.create(
                instructions=instructions,
                name=name,
                tools=tools,
                model=model,
            )
            self.assistant = AssistantObject(**assistant_data)  # Using the setter
            return self.assistant
        except Exception as e:
            raise ValueError("Failed to create assistant") from e


    def retrieve_assistant(self, assistant_id: str) -> AssistantObject:
        """
        Retrieves the assistant from id using the OpenAI client and sets the __assistant attribute.
        Returns:
            AssistantObject: An instance representing the retrieved assistant.
        Raises:
            ValueError: If the assistant retrieval fails or returns invalid data.
        """
        try:
            client = OpenAI()
            assistant_data = client.beta.assistants.retrieve(assistant_id)
            self.assistant = AssistantObject(**assistant_data)  # Using the setter
            return self.assistant
        except Exception as e:
            raise ValueError("Failed to retreive assistant") from e


    def modify_assistant(
        self, 
        instructions: str, 
        name: Optional[str], 
        tools: list[Tool], 
        model: str, 
        file_ids: list[Any] = field(default_factory=list)
    ) -> AssistantObject:
        """
        Modifies the assistant's details.

        Parameters:
            instructions (str): New instructions for the assistant.
            name (Optional[str]): New name of the assistant.
            tools (List[Tool]): List of tools to be associated with the assistant.
            model (str): Model identifier.
            file_ids (List[Any]): List of file IDs associated with the assistant.

        Returns:
            AssistantObject: An instance representing the updated assistant.

        Raises:
            ValueError: If assistant modification fails or returns invalid data.
        """
        try:
            client = OpenAI()
            updated_assistant_data = client.beta.assistants.update(
                assistant_id=self.assistant.id,
                instructions=instructions,
                name=name,
                tools=[tool.__dict__ for tool in tools],  # Convert Tool objects to dictionaries
                model=model,
                file_ids=file_ids
            )
            return AssistantObject(**updated_assistant_data)
        except Exception as e:
            raise ValueError("Failed to modify assistant") from e

