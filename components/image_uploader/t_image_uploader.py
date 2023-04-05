
import pytest
import base64
from fastapi import UploadFile
from io import BytesIO
from pydantic import ValidationError

from components.image_uploader import (
    ImageUploader,
    ImageUploaderInputDict,
    ImageUploaderOutputDict,
)

# Helper function to create an UploadFile object with the given content and file name
def create_upload_file(content: str, file_name: str) -> UploadFile:
    return UploadFile(file_name, content=BytesIO(content.encode("utf-8")))


# Test cases for the ImageUploader component
test_data = [
    ("some_image_data", "image.jpg", "some_image_data_base64", "jpg"),
    ("invalid_image_data", "image.bmp", "invalid_image_data_base64", None),
]

# Test inputs and expected output values for the ImageUploader component
@pytest.mark.parametrize(
    "input_content,input_filename,expected_content_base64,expected_file_format",
    test_data,
)
def test_image_uploader_transform(
    input_content, input_filename, expected_content_base64, expected_file_format
):

    # Create an ImageUploader instance
    image_uploader = ImageUploader()

    # Create an UploadFile input object with the mocked input content and file name
    input_file = create_upload_file(input_content, input_filename)

    # Call the ImageUploader transform method with the mocked input data
    if expected_file_format is None:
        with pytest.raises(ValueError, match="Unsupported file format"):
            image_uploader.transform(args=ImageUploaderInputDict(image=input_file))
    else:
        output_data = image_uploader.transform(
            args=ImageUploaderInputDict(image=input_file)
        )

        # Verify that the output data matches the expected values
        assert output_data == ImageUploaderOutputDict(
            filename=input_filename,
            content_base64=base64.b64encode(input_content.encode("utf-8")).decode(
                "utf-8"
            ),
            file_format=expected_file_format,
        )


# Error handling test case - invalid input file
def test_image_uploader_invalid_input_file():

    # Create an ImageUploader instance
    image_uploader = ImageUploader()

    # Create an invalid UploadFile input object
    invalid_input_file = "invalid_content"

    # Call the ImageUploader transform method with the invalid input file and check for ValidationError
    with pytest.raises(ValidationError):
        image_uploader.transform(args=ImageUploaderInputDict(image=invalid_input_file))
