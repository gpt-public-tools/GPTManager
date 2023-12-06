from dataclasses import dataclass
from openai import OpenAI
from typing import Optional
from GPTManager.Client import Client


@dataclass
class Image:
    """
    A class representing an image.

    Attributes:
        b64_json (str): The base64 encoded JSON data.
        url (str): The URL of the image.
        revised_prompt (str): The revised prompt used to create the image.

    Methods:
        create_image(model: str, prompt: str, n: int, size: str): Creates an image.
        create_image_edit(image: str, mask: str, prompt: str, n: int, size: str): Creates an edited image.
        create_image_variation(image: str, n: int, size: str): Creates a variation of an image.
    """
    b64_json: Optional[str]
    url: str
    revised_prompt: Optional[str]


    def create_image(self, prompt: str, model: str = None, n: int = None, size: str = None):
        """
        Creates an image.

        Parameters:
            model (str): The model to use.
            prompt (str): The prompt to use.
            n (int): The number of images to create.
            size (str): The size of the image.

        Returns:
            None

        Raises:
            ValueError: If the image creation fails or returns invalid data.
        """
        client = Client.get_instance()

        try:
            kwargs = {
                "prompt": prompt,
            }
            if model is not None:
                kwargs["model"] = model
            if n is not None:
                kwargs["n"] = n
            if size is not None:
                kwargs["size"] = size

            image_data = client.images.generate(**kwargs)

            self.b64_json = image_data.get('b64_json', '')
            self.url = image_data['url']
            self.revised_prompt = image_data.get('revised_prompt', '')
        except Exception as e:
            raise ValueError(f'Unable to create image: {e}')
        
    def create_image_edit(self, image: str, mask: str, prompt: str, n: int, size: str):
        """
        Creates an edited image.

        Parameters:
            image (str): The path to the image to edit.
            mask (str): The path to the image mask.
            prompt (str): The prompt to use.
            n (int): The number of images to create.
            size (str): The size of the image.

        Returns:
            None

        Raises:
            ValueError: If the image creation fails or returns invalid data.
        """
        client = Client.get_instance()

        try:
            image_data = client.images.edit(
                image=open(image, "rb"),
                mask=open(mask, "rb"),
                prompt=prompt,
                n=n,
                size=size
            )

            self.b64_json = image_data['b64']
            self.url = image_data['url']
            self.revised_prompt = image_data['revised_prompt']
        except Exception as e:
            raise ValueError(f'Unable to create image: {e}')
        
    def create_image_variation(self, image: str, n: int, size: str):
        """
        Creates a variation of an image.
        
        Parameters:
            image (str): The path to the image to create a variation of.
            n (int): The number of variations to create.
            size (str): The size of the image.
            
        Returns:
            None
                
        Raises:
            ValueError: If the image creation fails or returns invalid data.
        """
        client = Client.get_instance()

        try:
            image_data = client.images.create_variation(
                image=open(image, "rb"),
                n=n,
                size=size
            )

            self.b64_json = image_data['b64']
            self.url = image_data['url']
            self.revised_prompt = image_data['revised_prompt']
        except Exception as e:
            raise ValueError(f'Unable to create image: {e}')