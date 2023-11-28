from openai import OpenAI

from dataclasses import dataclass, field
from typing import Any

@dataclass
class TextContent:
    value: str
    annotations: list[Any] = field(default_factory=list)

@dataclass
class Content:
    type: str
    text: TextContent

@dataclass
class Message:
    id: str
    object: str
    created_at: int
    thread_id: str
    role: str
    content: list[Content]
    file_ids: list[Any] = field(default_factory=list)
    assistant_id: str
    run_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

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
    file_id: str

class Thread:
    """
    A class representing a thread.

    Attributes:
        __id (str): The unique identifier of the thread.
        __object (str): The type of object, always 'thread'.
        __created_at (int): The timestamp of thread creation.
        __metadata (dict): A dictionary containing the metadata of the thread.
    
    Methods:
        create_thread(): Creates a new thread using the OpenAI client and sets the __id, __object, __created_at and __metadata attributes.
        retrieve_thread(): Retrieves the thread from id using the OpenAI client and sets the __id, __object, __created_at and __metadata attributes.
        modify_thread(): Modifies the thread  using the OpenAI client and sets the __metadata attribute.
        delete_thread(): Deletes the thread using the OpenAI client and sets the __thread to None.
        create_message(): Creates a message for the thread, either from a Message or by specifying individual parameters.
        retrieve_message(): Retrieves a message from the thread using the message ID.
        modify_message_metadata(): Modifies the metadata of a specific message identified by its ID.
        list_thread_messages(): Retrieves a list of messages from the current thread.
        retrieve_message_file(): Retrieves a specific file associated with a message in the thread.
        list_message_files(): Lists all files associated with a specific message in the thread.
        upload_file(): Uploads a file to the thread.
        wait_runs(): Waits for all runs in the thread to complete.
    """
    __id: str
    __object: str
    __created_at: int
    __metadata: dict[str, Any] = field(default_factory=dict)


    def __init__(self, thread_id: str|None = None):
        """
        Initializes a new thread object.
        Parameters:
            thread_id (str): The id of the thread to be retrieved.
        Returns:
            None
        """
        if thread_id is not None:
            self.__id = thread_id
            self.retrieve_thread()
        else:
            self.create_thread()


    def create_thread(self):
        """
        Creates a new thread using the OpenAI client and sets the __id, __object, __created_at and __metadata attributes.
        Parameters:
            None
        Returns:
            None

        Raises:
            ValueError: If the thread creation fails or returns invalid data.
        """
        try:
            client = OpenAI()
            thread_data = client.beta.threads.create()
            self.__id = thread_data.get('id', None)
            self.__object = thread_data.get('object', None)
            self.__created_at = thread_data.get('created_at', None)
            self.__metadata = thread_data.get('id', None)
        except Exception as e:
            raise ValueError("Failed to create thread") from e


    def retrieve_thread(self):
        """
        Retrieves the thread from id using the OpenAI client and sets the __id, __object, __created_at and __metadata attributes.
        
        Returns:
            None

        Raises:
            ValueError: If the thread retrieval fails or returns invalid data.
        """
        try:
            client = OpenAI()
            thread_data = client.beta.threads.retrieve(self.__id)
            self.__object = thread_data.get('object', None)
            self.__created_at = thread_data.get('created_at', None)
            self.__metadata = thread_data.get('id', None)
        except Exception as e:
            raise ValueError("Failed to retreive thread") from e


    def modify_thread(self, metadata: dict):   
        """
        Modifies the thread  using the OpenAI client and sets the __metadata attribute.
        
        Returns:
            None   
             
        Raises:
            ValueError: If the thread modification fails or returns invalid data.
        """
        try:
            client = OpenAI()
            thread_data = client.beta.threads.update(
                thread_id = self.__id, 
                metadata = metadata
            )
            self.__metadata = thread_data.get('id', None)
        except Exception as e:
            raise ValueError("Failed to modify thread metadata") from e


    def delete_thread(self) -> dict: 
        """     
        Deletes the thread using the OpenAI client and sets the __thread to None.
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
            client = OpenAI()
            return client.beta.threads.delete(self.__id)
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
            return self.__create_message_from_message(message=kwargs['message'])
        elif 'role' in kwargs and 'content' in kwargs:
            file_ids = kwargs.get('file_ids', [])
            return self.__create_message_from_params(role=kwargs['role'], content=kwargs['content'], file_ids=file_ids)
        return None


    def __create_message_from_message(self, message: Message) -> Message:
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
            client = OpenAI()
            message_data = client.beta.threads.messages.create(
                message.thread_id,
                role=message.role,
                content=message.content,
                file_ids=message.file_ids
            )
            return Message(**message_data)
        except Exception as e:
            raise ValueError("Failed to create message from Message") from e


    def __create_message_from_params(self, role, content: str, file_ids = []) -> Message:
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
            client = OpenAI()
            message_data = client.beta.threads.messages.create(
                self.thread.id,
                role=role,
                content=content,
                file_ids=file_ids 
            )
            return Message(**message_data) 
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
            client = OpenAI()
            message_data = client.beta.threads.messages.retrieve(
                message_id=message_id,
                thread_id=self.thread.id
            )
            return Message(**message_data)
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
            client = OpenAI()
            message_data = client.beta.threads.messages.update(
                message_id=message_id,
                thread_id=self.thread.id,
                metadata=metadata
            )
            return Message(**message_data)
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
            client = OpenAI()
            messages_data = client.beta.threads.messages.list(self.thread.id)
            return [Message(**message) for message in messages_data]
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
            client = OpenAI()
            file_data = client.beta.threads.messages.files.retrieve(
                thread_id=self.thread.id,
                message_id=message_id,
                file_id=file_id
            )
            return MessageFile(**file_data)
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
            client = OpenAI()
            files_data = client.beta.threads.messages.files.list(
                thread_id=self.thread.id,
                message_id=message_id
            )
            return [MessageFile(**file) for file in files_data]
        except Exception as e:
            raise ValueError("Failed to list message files") from e


    def upload_file(self):
        pass


    def wait_runs(self):
        pass


