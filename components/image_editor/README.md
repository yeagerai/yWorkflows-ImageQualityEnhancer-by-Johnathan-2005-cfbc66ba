
# ImageEditor

Applies the suggested edits from AIModel to the input image, generating an enhanced image preview. Outputs the enhanced image, its filename, and file format.

## Initial generation prompt
description: Applies the suggested edits from AIModel to the input image, generating
  an enhanced image preview. Outputs the enhanced image, its filename, and file format.
input_from: AIModel
name: ImageEditor


## Transformer breakdown
- 1. Validate input_image and suggested_edits
- 2. Initialize an image editing library
- 3. Apply each suggested edit from the AIModel to the input_image using the editing library
- 4. Generate the enhanced_image by finalizing the edits
- 5. Extract filename and file_format from the enhanced_image
- 6. Return enhanced_image, filename, and file_format

## Parameters
[]

        