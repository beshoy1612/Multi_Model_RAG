from LLMinterface import LLMinterface
from google import genai
from PIL import Image

import logging


class GeminiVLMProvider(LLMinterface):

    def __init__(self,api_key: str,default_output_max_tokens: int = 1000):

        self.api_key = api_key

        self.default_output_max_tokens = (
            default_output_max_tokens
        )

        # VLM model
        self.vlm_model_id = None


        # Initialize Gemini client
        self.client = genai.Client(
            api_key=self.api_key
        )


        self.logger = logging.getLogger(__name__)


    # =================================
    # VLM Model
    # =================================

    def set_vlm_model(self,model_id: str):

        self.vlm_model_id = model_id


    # =================================
    # Image Analysis
    # =================================

    def analyze_image(self,image,prompt: str):

        if not self.client:

            self.logger.error(
                "Gemini client was not found"
            )

            return None


        if not self.vlm_model_id:

            self.logger.error(
                "VLM model was not found"
            )

            return None


        try:

            # Open image
            image = Image.open(image)


            response = (
                self.client.models.generate_content(

                    model=self.vlm_model_id,

                    contents=[
                        image,
                        prompt
                    ]
                )
            )


            if not response or not response.text:

                self.logger.error(
                    "Error while analyzing image with Gemini"
                )

                return None


            return response.text


        except Exception as error:

            self.logger.error(
                f"Error while analyzing image: {error}"
            )

            return None


    # =================================
    # Unsupported Functions
    # =================================

    def set_generation_model(self,model_id: str):
        raise NotImplementedError(
            "GeminiVLMProvider does not support text generation"
        )


    def set_embedding_model(self,model_id: str,embedding_size: int):

        raise NotImplementedError(
            "GeminiVLMProvider does not support embeddings"
        )


    def generate_text(self,prompt: str,max_output_tokens: int = None,chat_history: list = [],temperature: float = None):

        raise NotImplementedError(
            "GeminiVLMProvider does not support text generation"
        )


    def embed_text(self,text: str,document_type: str = None):

        raise NotImplementedError(
            "GeminiVLMProvider does not support embeddings"
        )



    def construct_prompt(
        self,
        prompt: str,
        role: str
    ):

        return {

            "role": role,

            "text": prompt
        }