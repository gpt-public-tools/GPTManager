from openai import OpenAI
from dataclasses import dataclass, field
from typing import Any

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GPTManager.Client import Client

import openai
import os
from dotenv import load_dotenv
load_dotenv()

@dataclass
class Message_Base:
    role: str
    content: list[Any]
    file_ids: list[str]

    def __init__(self, role: str, content: str, file_ids: list[str] = []):
        self.role = role
        self.file_ids = file_ids
        self.content = [
            {
                "type": "text",
                "text": {
                    "value": content,
                    "annotations": []
                }
            }
        ]


@dataclass
class Message(Message_Base):
    id: str
    object: str
    created_at: int
    thread_id: str
    role: str
    content: list[Any]
    file_ids: list[Any]
    assistant_id: str
    run_id: str
    metadata: dict[str, Any]   


@dataclass
class MessageFile:
    """
    A class representing a message file.

    Attributes:
        id (str): The unique identifier of the file.
        object (str): The type of object, always 'file'.
        created_at (int): The timestamp of file creation.
        message_id (str): The unique identifier of the message the file is associated with.
        file_id (str): The unique identifier of the file.
    """
    id: str
    object: str
    created_at: int
    message_id: str


class Thread:
    """
    A class representing a thread.

    Attributes:
        id (str): The unique identifier of the thread.
        object (str): The type of object, always 'thread'.
        created_at (int): The timestamp of thread creation.
        metadata (dict): A dictionary containing the metadata of the thread.
    
    Methods:
        create_thread(): Creates a new thread using the OpenAI client and sets the id, object, created_at and metadata attributes.
        retrieve_thread(): Retrieves the thread from id using the OpenAI client and sets the id, object, created_at and metadata attributes.
        modify_thread(): Modifies the thread  using the OpenAI client and sets the metadata attribute.
        delete_thread(): Deletes the thread using the OpenAI client and sets the thread to None.
        create_message(): Creates a message for the thread, either from a Message or by specifying individual parameters.
        retrieve_message(): Retrieves a message from the thread using the message ID.
        modify_message_metadata(): Modifies the metadata of a specific message identified by its ID.
        list_thread_messages(): Retrieves a list of messages from the current thread.
        retrieve_message_file(): Retrieves a specific file associated with a message in the thread.
        list_message_files(): Lists all files associated with a specific message in the thread.
        upload_file(): Uploads a file to the thread.
        wait_runs(): Waits for all runs in the thread to complete.
    """
    id: str
    object: str
    created_at: int
    metadata: dict[str, Any] = field(default_factory=dict)


    def __init__(self, thread_id: str|None = None) -> 'Thread':
        """
        Initializes a new thread object.
        Parameters:
            thread_id (str): The id of the thread to be retrieved.
        Returns:
            None
        """
        if thread_id is not None:
            self.id = thread_id
            self.retrieve_thread()
        else:
            self.create_thread()


    def create_thread(self):
        """
        Creates a new thread using the OpenAI client and sets the id, object, created_at and metadata attributes.
        Parameters:
            None
        Returns:
            None

        Raises:
            ValueError: If the thread creation fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            thread_data = client.beta.threads.create()
            self.id = thread_data.id
            self.object = thread_data.object
            self.created_at = thread_data.created_at
            self.metadata = thread_data.metadata
        except Exception as e:
            raise ValueError("Failed to create thread") from e


    def retrieve_thread(self):
        """
        Retrieves the thread from id using the OpenAI client and sets the id, object, created_at and metadata attributes.
        
        Returns:
            None

        Raises:
            ValueError: If the thread retrieval fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            thread_data = client.beta.threads.retrieve(self.id)
            self.object = thread_data.object
            self.created_at = thread_data.created_at
            self.metadata = thread_data.metadata
        except Exception as e:
            raise ValueError("Failed to retreive thread") from e


    def modify_thread(self, metadata: dict):   
        """
        Modifies the thread  using the OpenAI client and sets the metadata attribute.
        
        Returns:
            None   
             
        Raises:
            ValueError: If the thread modification fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            thread_data = client.beta.threads.update(
                thread_id = self.id, 
                metadata = metadata
            )
            self.metadata = thread_data.metadata
        except Exception as e:
            raise ValueError("Failed to modify thread metadata") from e


    def delete_thread(self) -> dict: 
        """     
        Deletes the thread using the OpenAI client and sets the thread to None.
        Returns:
            {
                "id": "thread_abc123",
                "object": "thread.deleted",
                "deleted": true
            }
        Raises:
            ValueError: If the thread modification fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            return client.beta.threads.delete(self.id)
        except Exception as e:
            raise ValueError("Failed to delete thread") from e

   
    def create_message(self, **kwargs) -> Message:
        """
        Creates a message for the thread, either from a Message or by specifying individual parameters.

        This method can accept a Message directly, or a combination of 'role', 'content', and optionally 'file_ids'.
        
        Parameters:
            kwargs: A dictionary of keyword arguments. This can include:
                - message (Message): An instance of Message containing message details.
                - role (str): The role of the message sender (required if message is not provided).
                - content (str): The content of the message (required if message is not provided).
                - file_ids (list): A list of file IDs to be attached to the message (optional).

        Returns:
            Message: An instance representing the created message, or None if required parameters are missing.

        Raises:
            ValueError: If message creation fails or returns invalid data.
        """
        if 'message' in kwargs:
            return self.__create_message_from_message_object(message=kwargs['message'])
        elif 'role' in kwargs and 'content' in kwargs:
            file_ids = kwargs.get('file_ids', [])
            return self.__create_message_from_params(role=kwargs['role'], content=kwargs['content'], file_ids=file_ids)
        return None


    def __create_message_from_message_object(self, message: Message_Base) -> Message:
        """     
        Creates a message for the thread using a Message.

        Parameters:
            message (Message): An instance of Message containing message details.

        Returns:
            Message: An instance representing the created message.

        Raises:
            ValueError: If message creation fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            message_data = client.beta.threads.messages.create(
                thread_id=self.id,
                role=message.role,
                content=message.content,
                file_ids=message.file_ids
            )
            
            return Message(
                id=message_data.id,
                role=message_data.role,
                object=message_data.object,
                created_at=message_data.created_at,
                thread_id=message_data.thread_id,
                content=message_data.content,
                file_ids=message_data.file_ids,
                assistant_id=message_data.assistant_id,
                run_id=message_data.run_id,
                metadata=message_data.metadata,
            )
        except Exception as e:
            raise ValueError("Failed to create message from Message") from e


    def __create_message_from_params(self, role: str, content: str, file_ids = []) -> Message:
        """     
        Creates a message for the thread using the provided parameters.

        Parameters:
            role (str): The role of the message sender.
            content (str): The content of the message.
            file_ids (list): A list of file IDs to be attached to the message.

        Returns:
            Message: An instance representing the created message.

        Raises:
            ValueError: If message creation fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            message_data = client.beta.threads.messages.create(
                self.id,
                role=role,
                content=content,
                file_ids=file_ids 
            )

            return Message(
                id=message_data.id,
                role=message_data.role,
                object=message_data.object,
                created_at=message_data.created_at,
                thread_id=message_data.thread_id,
                content=message_data.content,
                file_ids=message_data.file_ids,
                assistant_id=message_data.assistant_id,
                run_id=message_data.run_id,
                metadata=message_data.metadata,
            )
        except Exception as e:
            raise ValueError("Failed to create message") from e
    

    def retrieve_message(self, message_id: str) -> Message:
        """
        Retrieves a message from the thread using the message ID.

        Parameters:
            message_id (str): The unique identifier of the message to be retrieved.

        Returns:
            Message: An instance representing the retrieved message.

        Raises:
            ValueError: If message retrieval fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            message_data = client.beta.threads.messages.retrieve(
                message_id=message_id,
                thread_id=self.id
            )

            return Message(
                id=message_data.id,
                role=message_data.role,
                object=message_data.object,
                created_at=message_data.created_at,
                thread_id=message_data.thread_id,
                content=message_data.content,
                file_ids=message_data.file_ids,
                assistant_id=message_data.assistant_id,
                run_id=message_data.run_id,
                metadata=message_data.metadata,
            )
        except Exception as e:
            raise ValueError("Failed to retrieve message") from e


    def modify_message_metadata(self, message_id: str, metadata: dict) -> Message:
        """
        Modifies the metadata of a specific message identified by its ID.

        Parameters:
            message_id (str): The unique identifier of the message to be modified.
            metadata (dict): A dictionary containing the metadata to be updated.

        Returns:
            Message: An instance representing the updated message.

        Raises:
            ValueError: If message metadata modification fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            message_data = client.beta.threads.messages.update(
                message_id=message_id,
                thread_id=self.id,
                metadata=metadata
            )
            
            return Message(
                id=message_data.id,
                role=message_data.role,
                object=message_data.object,
                created_at=message_data.created_at,
                thread_id=message_data.thread_id,
                content=message_data.content,
                file_ids=message_data.file_ids,
                assistant_id=message_data.assistant_id,
                run_id=message_data.run_id,
                metadata=message_data.metadata,
            )
        except Exception as e:
            raise ValueError("Failed to modify message metadata") from e


    def list_thread_messages(self) -> list[Message]:
        """
        Retrieves a list of messages from the current thread.

        Returns:
            list[Message]: A list of Message instances representing the messages in the thread.

        Raises:
            ValueError: If the retrieval of thread messages fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            messages_data = client.beta.threads.messages.list(self.id)
            return  [
                        Message(
                            id=message.id,
                            role=message.role,
                            object=message.object,
                            created_at=message.created_at,
                            thread_id=message.thread_id,
                            content=message.content,
                            file_ids=message.file_ids,
                            assistant_id=message.assistant_id,
                            run_id=message.run_id,
                            metadata=message.metadata,
                        ) 
                        for message 
                        in messages_data.data
                    ]
        except Exception as e:
            raise ValueError("Failed to retrieve thread messages") from e


    def retrieve_message_file(self, message_id: str, file_id: str) -> MessageFile:
        """
        Retrieves a specific file associated with a message in the thread.

        Parameters:
            message_id (str): The unique identifier of the message.
            file_id (str): The unique identifier of the file to be retrieved.

        Returns:
            MessageFile: An instance representing the retrieved file.

        Raises:
            ValueError: If file retrieval fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            file_data = client.beta.threads.messages.files.retrieve(
                thread_id=self.id,
                message_id=message_id,
                file_id=file_id
            )

            return MessageFile(
                id=file_data.id,
                object=file_data.object,                
                created_at=file_data.created_at,
                message_id=file_data.message_id
            )
        except Exception as e:
            raise ValueError("Failed to retrieve message file") from e


    def list_message_files(self, message_id: str) -> list[MessageFile]:
        """
        Lists all files associated with a specific message in the thread.

        Parameters:
            message_id (str): The unique identifier of the message whose files are to be listed.

        Returns:
            list[MessageFile]: A list of MessageFile instances representing the files associated with the message.

        Raises:
            ValueError: If file listing fails or returns invalid data.
        """
        try:
            client = Client.get_instance()
            files_data = client.beta.threads.messages.files.list(
                thread_id=self.id,
                message_id=message_id
            )
            return [
                        MessageFile(
                            id=message_file.id,
                            object=message_file.object,
                            created_at=message_file.created_at,
                            message_id=message_file.message_id
                        ) 
                        for message_file 
                        in files_data.data
                    ]
        except Exception as e:
            raise ValueError("Failed to list message files") from e


