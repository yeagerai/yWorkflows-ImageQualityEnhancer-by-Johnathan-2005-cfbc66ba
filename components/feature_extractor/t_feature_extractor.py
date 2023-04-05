
import pytest
import yaml
from base64 import b64encode
from PIL import Image
from io import BytesIO
from typing import Dict
from feature_extractor import FeatureExtractor, FeatureExtractorInputDict, FeatureExtractorOutputDict

def create_base64_image(width: int, height: int, color: str) -> str:
    image = Image.new(mode="RGB", size=(width, height), color=color)
    img_bytes = BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()
    return b64encode(img_bytes).decode("utf-8")

test_cases = [
    {
        "input": FeatureExtractorInputDict(base64_image_content=create_base64_image(100, 100, "red")),
        "output": {
            "brightness": 1.0,
            "contrast": 0.0,
            "color_balance": 1.0,
            "sharpness": 0.0
        }
    },
    {
        "input": FeatureExtractorInputDict(base64_image_content=create_base64_image(100, 100, "green")),
        "output": {
            "brightness": 0.0,
            "contrast": 1.0,
            "color_balance": 1.0,
            "sharpness": 0.0
        }
    },
]

@pytest.mark.parametrize(
    "test_case",
    test_cases,
    ids=lambda x: str(x["input"])
)
def test_feature_extractor(test_case: Dict) -> None:
    feature_extractor = FeatureExtractor()
    input_data = test_case["input"]
    expected_output = test_case["output"]

    # Call the transform method and get the output
    result = feature_extractor.transform(input_data)

    # Check if the output matches the expected output
    for key, value in expected_output.items():
        assert pytest.approx(result.image_features[key], 0.01) == value
        
    # Check if the output contains only the expected keys
    assert set(result.image_features.keys()) == set(expected_output.keys())

# Add more test functions for edge cases and error handling as needed
