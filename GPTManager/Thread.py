from openai import OpenAI

from Message import MessageObject

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
    message: MessageObject   

    def __init__(self, thread_id = None):
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


    def retrieve_thread(self, thread_id) -> ThreadObject:
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


    def modify_thread_metadata(self, thread_id, metadata) -> ThreadObject:   
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


    def create_message_from_params(self, role, content: str, file_ids) -> MessageObject:
        client = OpenAI()
        return client.beta.threads.messages.create(
            self.id,
            role=role,
            content=content,
            file_ids=[]
        )
    

    def create_message_from_message_object(self, message: MessageObject) -> MessageObject:
        client = OpenAI()
        return client.beta.threads.messages.create(
            message.thread_id,
            role=message.role,
            content=message.content,
            file_ids=message.file_ids
        )
    

    def upload_file(self):
        pass


    def get_messages(self) -> list[MessageObject]:
        pass


    def wait_runs(self):
        pass


