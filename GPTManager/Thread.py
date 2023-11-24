from openai import OpenAI

class Thread:
    __thread: dict  = None
    __apiKey: str = None
    id: str
    created_at: int
    metadata: dict

    def __init__(self, id = None):
        if id:
            self.retreive(id)
        else:
            self.create()

        self.__sync()

        pass

    def create(self):
        client = OpenAI()
        self.__thread = client.beta.threads.create()

    def retreive(self, id):
        client = OpenAI()
        self.__thread = client.beta.threads.retrieve(id)

    def modify(self, id, metadata):
        client = OpenAI()
        self.__thread = client.beta.threads.update(
            thread_id = id, 
            metadata = metadata
        )

    def delete(self, id):
        """     
        returns {
            "id": "thread_id",
            "object": "thread.deleted",
            "deleted": true
        }
        """
        client = OpenAI()
        return client.beta.threads.delete(id)


    def push_message(self):
        pass

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


