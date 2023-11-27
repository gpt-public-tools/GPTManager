from openai import OpenAI

from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class TextContent:
    value: str
    annotations: list[Any] = field(default_factory=list)

@dataclass
class Content:
    type: str
    text: TextContent

@dataclass
class MessageObject:
    id: str
    object: str
    created_at: int
    thread_id: str
    role: str
    content: list[Content]
    file_ids: list[Any] = field(default_factory=list)
    assistant_id: str
    run_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MessageFileObject:
    id: str
    object: str
    created_at: int
    message_id: str
    file_id: str

class Thread:
    __id: str
    __object: str
    __created_at: int
    __metadata: Dict[str, Any] = field(default_factory=dict)


    def __init__(self, thread_id: str|None = None):
        if thread_id is not None:
            self.__id = thread_id
            self.retrieve_thread()
        else:
            self.create_thread()


    def create_thread(self):
        """
        Creates a new thread using the OpenAI client and sets the __id, __object, __created_at and __metadata attributes.
        
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
            self.__created_at = thread_data.get('object', None)
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
            self.__created_at = thread_data.get('object', None)
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


    def delete_thread(self, thread_id): 
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
            self.__id = None
            self.__object = None
            self.__created_at = None
            self.__metadata = None
            return client.beta.threads.delete(thread_id)
        except Exception as e:
            raise ValueError("Failed to delete thread") from e

   
    def create_message(self, **kwargs) -> MessageObject:
        """
        Creates a message for the thread, either from a MessageObject or by specifying individual parameters.

        This method can accept a MessageObject directly, or a combination of 'role', 'content', and optionally 'file_ids'.
        
        Parameters:
            kwargs: A dictionary of keyword arguments. This can include:
                - message_object (MessageObject): An instance of MessageObject containing message details.
                - role (str): The role of the message sender (required if message_object is not provided).
                - content (str): The content of the message (required if message_object is not provided).
                - file_ids (list): A list of file IDs to be attached to the message (optional).

        Returns:
            MessageObject: An instance representing the created message, or None if required parameters are missing.

        Raises:
            ValueError: If message creation fails or returns invalid data.
        """
        if 'message_object' in kwargs:
            return self.__create_message_from_message_object(message_object=kwargs['message_object'])
        elif 'role' in kwargs and 'content' in kwargs:
            file_ids = kwargs.get('file_ids', [])
            return self.__create_message_from_params(role=kwargs['role'], content=kwargs['content'], file_ids=file_ids)
        return None


    def __create_message_from_message_object(self, message_object: MessageObject) -> MessageObject:
        """     
        Creates a message for the thread using a MessageObject.

        Parameters:
            message (MessageObject): An instance of MessageObject containing message details.

        Returns:
            MessageObject: An instance representing the created message.

        Raises:
            ValueError: If message creation fails or returns invalid data.
        """
        try:
            client = OpenAI()
            message_data = client.beta.threads.messages.create(
                message_object.thread_id,
                role=message_object.role,
                content=message_object.content,
                file_ids=message_object.file_ids
            )
            return MessageObject(**message_data)
        except Exception as e:
            raise ValueError("Failed to create message from MessageObject") from e


    def __create_message_from_params(self, role, content: str, file_ids = []) -> MessageObject:
        """     
        Creates a message for the thread using the provided parameters.

        Parameters:
            role (str): The role of the message sender.
            content (str): The content of the message.
            file_ids (list): A list of file IDs to be attached to the message.

        Returns:
            MessageObject: An instance representing the created message.

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
            return MessageObject(**message_data) 
        except Exception as e:
            raise ValueError("Failed to create message") from e
    

    def retrieve_message(self, message_id: str) -> MessageObject:
        """
        Retrieves a message from the thread using the message ID.

        Parameters:
            message_id (str): The unique identifier of the message to be retrieved.

        Returns:
            MessageObject: An instance representing the retrieved message.

        Raises:
            ValueError: If message retrieval fails or returns invalid data.
        """
        try:
            client = OpenAI()
            message_data = client.beta.threads.messages.retrieve(
                message_id=message_id,
                thread_id=self.thread.id
            )
            return MessageObject(**message_data)
        except Exception as e:
            raise ValueError("Failed to retrieve message") from e


    def modify_message_metadata(self, message_id: str, metadata: dict) -> MessageObject:
        """
        Modifies the metadata of a specific message identified by its ID.

        Parameters:
            message_id (str): The unique identifier of the message to be modified.
            metadata (dict): A dictionary containing the metadata to be updated.

        Returns:
            MessageObject: An instance representing the updated message.

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
            return MessageObject(**message_data)
        except Exception as e:
            raise ValueError("Failed to modify message metadata") from e


    def list_thread_messages(self) -> list[MessageObject]:
        """
        Retrieves a list of messages from the current thread.

        Returns:
            list[MessageObject]: A list of MessageObject instances representing the messages in the thread.

        Raises:
            ValueError: If the retrieval of thread messages fails or returns invalid data.
        """
        try:
            client = OpenAI()
            messages_data = client.beta.threads.messages.list(self.thread.id)
            return [MessageObject(**message) for message in messages_data]
        except Exception as e:
            raise ValueError("Failed to retrieve thread messages") from e


    def retrieve_message_file(self, message_id: str, file_id: str) -> MessageFileObject:
        """
        Retrieves a specific file associated with a message in the thread.

        Parameters:
            message_id (str): The unique identifier of the message.
            file_id (str): The unique identifier of the file to be retrieved.

        Returns:
            MessageFileObject: An instance representing the retrieved file.

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
            return MessageFileObject(**file_data)
        except Exception as e:
            raise ValueError("Failed to retrieve message file") from e


    def list_message_files(self, message_id: str) -> list[MessageFileObject]:
        """
        Lists all files associated with a specific message in the thread.

        Parameters:
            message_id (str): The unique identifier of the message whose files are to be listed.

        Returns:
            list[MessageFileObject]: A list of MessageFileObject instances representing the files associated with the message.

        Raises:
            ValueError: If file listing fails or returns invalid data.
        """
        try:
            client = OpenAI()
            files_data = client.beta.threads.messages.files.list(
                thread_id=self.thread.id,
                message_id=message_id
            )
            return [MessageFileObject(**file) for file in files_data]
        except Exception as e:
            raise ValueError("Failed to list message files") from e


    def upload_file(self):
        pass


    def wait_runs(self):
        pass


