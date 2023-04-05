
import os
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
import yaml
import torch

from core.abstract_component import AbstractComponent


class AIModelInputDict(BaseModel):
    image_features: List[float]


class AIModelOutputDict(BaseModel):
    suggested_edits: List[str]


class AIModel(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()
        with open(self.component_configuration_path(), "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        self.pre_trained_model_path = yaml_data["parameters"]["pre_trained_model_path"]
        self.model = torch.load(self.pre_trained_model_path)

    def transform(self, args: AIModelInputDict) -> AIModelOutputDict:
        image_features = torch.Tensor(args.image_features).unsqueeze(0)
        enhancement_map = self.model(image_features)
        suggested_edits = self.process_enhancement_map(enhancement_map)
        return AIModelOutputDict(suggested_edits=suggested_edits)

    def process_enhancement_map(self, enhancement_map: torch.Tensor) -> List[str]:
        # Implement processing logic here to extract suggested image edit operations
        # from the enhancement map.
        # Replace the example list below with the actual list of suggested edit operations.
        example_suggested_edits = ["increase_saturation", "sharpen_edges"]
        return example_suggested_edits


load_dotenv()
ai_model_app = FastAPI()

@ai_model_app.post("/transform/")
async def transform(
    args: AIModelInputDict,
) -> AIModelOutputDict:
    ai_model = AIModel()
    return ai_model.transform(args)
