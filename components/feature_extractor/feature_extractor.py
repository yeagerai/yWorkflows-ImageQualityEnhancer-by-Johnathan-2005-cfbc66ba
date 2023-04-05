
import os
import yaml
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from base64 import b64decode
from io import BytesIO
from PIL import Image
from image_processing import brightness, contrast, color_balance, sharpness

from core.abstract_component import AbstractComponent

class FeatureExtractorInputDict(BaseModel):
    base64_image_content: str

class FeatureExtractorOutputDict(BaseModel):
    image_features: dict

class FeatureExtractor(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()
        with open(self.component_configuration_path(), "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        self.brightness_scale = float(yaml_data["parameters"]["brightness_scale"])
        self.contrast_scale = float(yaml_data["parameters"]["contrast_scale"])
        self.color_balance_scale = float(yaml_data["parameters"]["color_balance_scale"])
        self.sharpness_scale = float(yaml_data["parameters"]["sharpness_scale"])

    def transform(
        self, args: FeatureExtractorInputDict
    ) -> FeatureExtractorOutputDict:

        image_data = b64decode(args.base64_image_content)
        image = Image.open(BytesIO(image_data))

        brightness_value = brightness(image) * self.brightness_scale
        contrast_value = contrast(image) * self.contrast_scale
        color_balance_value = color_balance(image) * self.color_balance_scale
        sharpness_value = sharpness(image) * self.sharpness_scale

        image_features = {
            "brightness": brightness_value,
            "contrast": contrast_value,
            "color_balance": color_balance_value,
            "sharpness": sharpness_value
        }

        return FeatureExtractorOutputDict(image_features=image_features)

load_dotenv()
feature_extractor_app = FastAPI()

@feature_extractor_app.post("/transform/")
async def transform(
    args: FeatureExtractorInputDict,
) -> FeatureExtractorOutputDict:
    feature_extractor = FeatureExtractor()
    return feature_extractor.transform(args)
