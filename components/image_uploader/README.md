markdown
# Component Name
ImageUploader

# Description
ImageUploader is a component within a Yeager Workflow designed to upload an image file, convert it to a base64 encoded string, and return the filename, content as a base64 encoded string, and the file format. The component supports JPG, JPEG, PNG, and GIF file formats.

# Input and Output Models
The component utilizes two Pydantic models for input and output validation and serialization:

- `ImageUploaderInputDict` for inputs:
    - `image`: UploadFile, representing the image to be uploaded.

- `ImageUploaderOutputDict` for outputs:
    - `filename`: str, the original filename of the uploaded image.
    - `content_base64`: str, the base64 encoded content of the image.
    - `file_format`: str, the format of the uploaded image.

# Parameters
There are no parameters for the ImageUploader component.

# Transform Function
This component processes the input data through the `transform()` method, which performs the following steps:

1. Extract the file format from the input image's filename.
2. Check if the file format is supported (JPG, JPEG, PNG, or GIF). If not, raise a ValueError with the message "Unsupported file format".
3. Read the content of the input image file.
4. Convert the content of the image file to a base64 encoded string.
5. Return an instance of `ImageUploaderOutputDict` containing the image filename, the base64 encoded content, and the file format.

# External Dependencies
The component uses the following external libraries:

- `os`: to handle file operations.
- `base64`: to perform base64 encoding and decoding of image content.
- `fastapi`: to create a FastAPI application and use its features such as File and UploadFile.
- `pydantic`: to define input and output models for data validation and serialization.

# API Calls
There are no external API calls made by the ImageUploader component.

# Error Handling
The transform() method raises ValueError if the input image's file format is unsupported, with the error message "Unsupported file format".

# Examples
Below is an example of how to use the ImageUploader component within a Yeager Workflow:

1. Instantiate the ImageUploader component:

