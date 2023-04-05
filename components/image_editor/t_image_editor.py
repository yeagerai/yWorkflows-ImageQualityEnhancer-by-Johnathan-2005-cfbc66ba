
import pytest
from pydantic import ValidationError
from your_module_path import ImageEditorInputDict, ImageEditorOutputDict, ImageEditor

INPUTS = [
    (
        ImageEditorInputDict(input_image="image_data_1", suggested_edits=[{"operation": "resize", "value": "50%"}]),
        ImageEditorOutputDict(enhanced_image="edited_image_data_1", filename="edited_image_filename_1", file_format="png"),
    ),
    (
        ImageEditorInputDict(input_image="image_data_2", suggested_edits=[{"operation": "brightness", "value": "+20"}]),
        ImageEditorOutputDict(enhanced_image="edited_image_data_2", filename="edited_image_filename_2", file_format="png"),
    ),
]

INVALID_INPUTS = [
    {"input_image": "image_data_1", "suggested_edits": [{"operation": "invalid_operation", "value": "+20"}]},
    {"input_image": "image_data_2", "suggested_edits": [{"operation": "brightness", "value": None}]},
]

@pytest.mark.parametrize("input_data, expected_output", INPUTS)
def test_image_editor(input_data, expected_output):
    image_editor = ImageEditor()
    output = image_editor.transform(input_data)

    assert output == expected_output, f"Expected {expected_output} but got {output}"


@pytest.mark.parametrize("invalid_input", INVALID_INPUTS)
def test_image_editor_invalid_inputs(invalid_input):
    with pytest.raises(ValidationError):
        ImageEditorInputDict(**invalid_input)
