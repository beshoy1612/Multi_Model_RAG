from .LLMenum import LLMenum
from .Providers import CoHereProvider
from .Providers import GeminiVLMProvider

class LLMProviderFactory():
    def __init__(self,config: dict):
        self.config = config

    def create(self , provider: str):
        if provider == LLMenum.GEMENI.value:
            return GeminiVLMProvider(
                api_key = self.config.GEMINI_API_KEY,
                default_output_max_tokens =  self.config.default_output_max_tokens,
            )

        if provider == LLMenum.COHERE.value:    
            return CoHereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_max_character  = self.config.default_input_max_character,
                default_output_max_character =  self.config.default_output_max_character,
                default_generation_temprature = self.config.default_generation_temprature 
            )  
