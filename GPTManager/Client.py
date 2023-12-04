from openai import OpenAI


class Client:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = OpenAI()
        return cls._instance