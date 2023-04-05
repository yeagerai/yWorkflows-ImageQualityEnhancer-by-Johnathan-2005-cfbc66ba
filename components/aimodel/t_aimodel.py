
import os
import pytest
from pydantic import ValidationError
from typing import Tuple, List
from fastapi.testclient import TestClient
from fastapi import FastAPI
import yaml

from components.AI_model import AIModel, AIModelInputDict, AIModelOutputDict

# Import the 'ai_model_app' object from the component file
from components.AI_model import ai_model_app

# Use the ai_model_app object to initialize the TestClient
client = TestClient(ai_model_app)

# Test cases with mocked input and expected output data
test_cases = [
    (AIModelInputDict(image_features=[1.0, 2.0, 3.0]), AIModelOutputDict(suggested_edits=["increase_saturation", "sharpen_edges"])),
    (AIModelInputDict(image_features=[0.5, 2.5, 0.8]), AIModelOutputDict(suggested_edits=["increase_saturation", "sharpen_edges"])),
    (AIModelInputDict(image_features=[3.3, 4.4, 5.5]), AIModelOutputDict(suggested_edits=["increase_saturation", "sharpen_edges"])),
]

# Test cases for invalid input
invalid_test_cases = [
    {"image_features": "a_string_instead_of_list"},
    {"image_features": [1.0, "string_in_list", 3.0]},
]

@pytest.mark.parametrize("input_data, expected_output", test_cases)
def test_ai_model_transform(input_data: AIModelInputDict, expected_output: AIModelOutputDict):
    response = client.post("/transform/", json=input_data.dict())
    assert response.status_code == 200
    assert AIModelOutputDict(**response.json()) == expected_output

# Edge case and error handling scenarios
@pytest.mark.parametrize("invalid_input_data", invalid_test_cases)
def test_ai_model_transform_invalid_input(invalid_input_data):
    with pytest.raises(ValidationError):
        _ = AIModelInputDict(**invalid_input_data)
