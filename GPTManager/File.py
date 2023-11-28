from dataclasses import dataclass
from openai import OpenAI


from GPTManager import Account


@dataclass
class File:
    id: str
    object: str
    bytes: int
    created_at: int
    filename: str
    purpose: str

    def upload_file(self, file_path: str, purpose: str):
        """
        Uploads a file to the OpenAI API.

        Parameters:
            file_path (str): The path to the file to upload.
            purpose (str): The purpose of the file.

        Returns:
            None

        Raises:
            ValueError: If the file upload fails or returns invalid data.
        """
        self.purpose = purpose
        self.filename = file_path.split('/')[-1]

        client = OpenAI()

        try:
            file_data = client.files.create(
                file=open(file_path, 'rb'),
                purpose=purpose
            )

            self.id = file_data['id']
            self.object = file_data['object']
            self.bytes = file_data['bytes']
            self.created_at = file_data['created_at']

        except Exception as e:
            raise ValueError(f'Unable to create file: {e}')
        
    def delete_file(self) -> dict:
        """
        Deletes a file from the OpenAI API.
        
        Parameters:
            None

        Returns:
            Response from the OpenAI API as python dictionary.
            {id: str, object: str, deleted: bool}

        Raises:
            ValueError: If the file deletion fails or returns invalid data.
            """

        client = OpenAI()

        try:
            return client.files.delete(self.id)
        except Exception as e:
            raise ValueError(f'Unable to delete file: {e}')
        
    def retrieve_file(self) -> None:
        """
        Retrieves a file from the OpenAI API.
        
        Parameters:
            None

        Returns:
            None

        Raises:
            ValueError: If the file retrieval fails or returns invalid data.
            """

        client = OpenAI()

        try:
            file = client.files.retrieve(self.id)

            self.object = file['object']
            self.bytes = file['bytes']
            self.created_at = file['created_at']
            self.filename = file['filename']
            self.purpose = file['purpose']

        except Exception as e:
            raise ValueError(f'Unable to retrieve file: {e}')
        
    def retrieve_file_content(self) -> str:
        """
        Retrieves the content of a file from the OpenAI API.
        
        Parameters:
            None

        Returns:
            The content of the file as a string.

        Raises:
            ValueError: If the file content retrieval fails or returns invalid data.
        """

        client = OpenAI()

        try:
            file = client.files.retrieve(self.id)

            return file['bytes']

        except Exception as e:
            raise ValueError(f'Unable to retrieve file content: {e}')

  