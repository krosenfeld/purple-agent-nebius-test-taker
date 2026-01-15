import os
from openai import OpenAI
from dotenv import load_dotenv

from dataclasses import dataclass

load_dotenv()

MODELS = {"nemotron-3-nano-30b-a3b": "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"}
# nemotron-3-nano-30b-a3b

def get_client():
    return OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=os.environ.get("NEBIUS_API_KEY"),
    )


SYSTEM_PROMPT = """You are a helpful assistant."""


@dataclass
class NeBiusClient:
    model: str
    system_prompt: str | None = None

    def __post_init__(self):
        if self.system_prompt is None:
            self.system_prompt = SYSTEM_PROMPT

        # Parse the model name
        self.model = self.model.lower()
        if self.model in MODELS.keys():
            self.model_id = MODELS[self.model]
        elif self.model in MODELS.values():
            self.model_id = self.model
        else:
            raise ValueError(f"Model {self.model} not found")

        self.client = get_client()

    def _generate_raw_response(self, message: str):
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": [{"type": "text", "text": message}]},
            ],
        )
        return response

    def generate_response(self, message: str):
        response = self._generate_raw_response(message)
        return response.choices[0].message.content
