from openai import OpenAI

from Message import Message


class Thread:
    __thread: dict  = None
    thread_id: str
    created_at: int
    metadata: dict
    message: dict(
        id = "msg_abc123",
        object = "thread.message",
        created_at= 1698983503,
        thread_id = "thread_abc123",
        role= "assistant",
        content = dict[
            dict( 
                    type= "text",
                    text = dict(
                         value= "Hi! How can I help you today?",
                        annotations= []
                    )
                ),
        ],
        file_ids= [],
        assistant_id= "asst_abc123",
        run_id= "run_abc123",
        metadata= {}
    )
        
    def __init__(self, thread_id = None):
        if thread_id:
            self.retreive(thread_id)
        else:
            self.create()

        self.__sync()

    def create(self):
        client = OpenAI()
        self.__thread = client.beta.threads.create()

    def retreive(self, thread_id):
        client = OpenAI()
        self.__thread = client.beta.threads.retrieve(thread_id)

    def modify(self, thread_id, metadata):
        client = OpenAI()
        self.__thread = client.beta.threads.update(
            thread_id = thread_id, 
            metadata = metadata
        )

    def delete(self, thread_id): 
        """     
        returns {
            "id": "thread_abc123",
            "object": "thread.deleted",
            "deleted": true
        }
        """
        client = OpenAI()
        return client.beta.threads.delete(thread_id)


    def create_message(self, role, content: str, file_ids) -> Message:
        client = OpenAI()
        return client.beta.threads.messages.create(
            self.id,
            role=role,
            content=content,
            file_ids=[]
        )
    
    def create_message(self, message: Message) -> Message:
        client = OpenAI()
        return client.beta.threads.messages.create(
            message.thread_id,
            role=message.role,
            content=message.content,
            file_ids=message.file_ids
        )
    
    def upload_file(self):
        pass

    def get_messages(self):
        pass

    def wait_runs(self):
        pass

    def __sync(self):
        self.id = self.__thread.id
        self.created_at = self.__thread.created_at
        self.metadata = self.__thread.metadata


