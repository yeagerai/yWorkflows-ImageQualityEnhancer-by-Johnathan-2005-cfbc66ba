
import pytest
from PIL import Image
from io import BytesIO
from pydantic import ValidationError
from urllib.error import HTTPError

from .comparison_presenter import (
    ComparisonPresenter,
    ComparisonPresenterInputDict,
    ComparisonPresenterOutputDict,
)

# Define mocked input and output data

mocked_original_image = Image.new("RGB", (100, 100), "white")
mocked_edited_image = Image.new("RGB", (100, 100), "black")
mocked_edits = ["invert colors", "resize"]

buffered_original = BytesIO()
buffered_edited = BytesIO()
mocked_original_image.save(buffered_original, format="PNG")
mocked_edited_image.save(buffered_edited, format="PNG")
mocked_original_image_bytes = buffered_original.getvalue()
mocked_edited_image_bytes = buffered_edited.getvalue()

mocked_input_data = ComparisonPresenterInputDict(
    original_image=mocked_original_image_bytes,
    edited_image=mocked_edited_image_bytes,
    edits=mocked_edits,
)

mocked_output_image = Image.new("RGB", (200, 100))
mocked_output_image.paste(mocked_original_image, (0, 0))
mocked_output_image.paste(mocked_edited_image, (100, 0))
buffered_output = BytesIO()
mocked_output_image.save(buffered_output, format="PNG")
mocked_output_image_bytes = buffered_output.getvalue()

mocked_output_data = ComparisonPresenterOutputDict(
    comparison_image=mocked_output_image_bytes,
    edit_summary="Edits applied: invert colors, resize",
)

test_data = [
    (mocked_input_data, mocked_output_data),
    # Add more test cases here
]

# Create test scenarios using @pytest.mark.parametrize

@pytest.mark.parametrize("input_data,expected_output", test_data)
def test_comparison_presenter(input_data, expected_output):
    """
    Test the ComparisonPresenter's transform() method with mocked input data.
    """
    comparison_presenter = ComparisonPresenter()
    result = comparison_presenter.transform(input_data)

    # Compare output images by converting to Image objects
    expected_output_image = Image.open(BytesIO(expected_output.comparison_image))
    result_output_image = Image.open(BytesIO(result.comparison_image))

    assert expected_output_image == result_output_image
    assert expected_output.edit_summary == result.edit_summary

# Error handling and edge case scenarios

def test_invalid_input_data():
    """
    Test the ComparisonPresenter with invalid input data, expecting a ValidationError.
    """
    invalid_input_data = {
        "original_image": mocked_original_image_bytes,
        "edited_image": mocked_edited_image_bytes,
        "edits": 123  # Invalid data type
    }
    with pytest.raises(ValidationError):
        ComparisonPresenterInputDict(**invalid_input_data)

def test_image_error_handling(monkeypatch):
    """
    Test the ComparisonPresenter when an Image handling error occurs.
    """
    def mock_open(*args, **kwargs):
        raise IOError("Image open error")

    monkeypatch.setattr(Image, "open", mock_open)

    with pytest.raises(IOError):
        comparison_presenter = ComparisonPresenter()
        comparison_presenter.transform(mocked_input_data)
