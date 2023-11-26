from openai import OpenAI

from Message import MessageObject, MessageFileObject

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ThreadObject:
    id: str
    object: str
    created_at: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    
class Thread:
    __thread: ThreadObject  = None

    def __init__(self, thread_id: str = None):
        if thread_id:
            self.retrieve_thread(thread_id)
        else:
            self.create_thread()


    @property
    def thread(self) -> ThreadObject:
        """Getter for __thread"""
        return self.__thread


    @thread.setter
    def thread(self, value: ThreadObject):
        """Setter for __thread"""
        if not isinstance(value, ThreadObject):
            raise ValueError("Value must be an instance of ThreadObject")
        self.__thread = value

  
    def create_thread(self) -> ThreadObject:
        """
        Creates a new thread using the OpenAI client and sets the __thread attribute.
        Returns:
            ThreadObject: An instance representing the newly created thread.
        Raises:
            ValueError: If the thread creation fails or returns invalid data.
        """
        try:
            client = OpenAI()
            thread_data = client.beta.threads.create()
            self.thread = ThreadObject(**thread_data)  # Using the setter
            return self.thread
        except Exception as e:
            raise ValueError("Failed to create thread") from e


    def retrieve_thread(self, thread_id: str) -> ThreadObject:
        """
        Retrieves the thread from id using the OpenAI client and sets the __thread attribute.
        Returns:
            ThreadObject: An instance representing the retrieved thread.
        Raises:
            ValueError: If the thread retrieval fails or returns invalid data.
        """
        try:
            client = OpenAI()
            thread_data = client.beta.threads.retrieve(thread_id)
            self.thread = ThreadObject(**thread_data)  # Using the setter
            return self.thread
        except Exception as e:
            raise ValueError("Failed to retreive thread") from e


    def modify_thread_metadata(self, thread_id: str, metadata: dict) -> ThreadObject:   
        """
        Modifies the thread  using the OpenAI client and sets the __thread.metadata attribute.
        Returns:
            ThreadObject: An instance representing the modified thread.
        Raises:
            ValueError: If the thread modification fails or returns invalid data.
        """
        try:
            client = OpenAI()
            thread_data = client.beta.threads.update(
                thread_id = thread_id, 
                metadata = metadata
            )
            self.thread = ThreadObject(**thread_data)  # Using the setter
            return self.thread
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
            self.thread = None
            return client.beta.threads.delete(thread_id)
        except Exception as e:
            raise ValueError("Failed to delete thread") from e


    def create_message_from_params(self, role, content: str, file_ids = []) -> MessageObject:
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
    
    
    def create_message_from_message_object(self, message: MessageObject) -> MessageObject:
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
                message.thread_id,
                role=message.role,
                content=message.content,
                file_ids=message.file_ids
            )
            return MessageObject(**message_data)
        except Exception as e:
            raise ValueError("Failed to create message from MessageObject") from e


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


