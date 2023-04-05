
# FeatureExtractor

Takes input as the base64 image content, processes the image and extracts relevant features such as brightness, contrast, color balance, and sharpness. Outputs the resulting features.

## Initial generation prompt
description: Takes input as the base64 image content, processes the image and extracts
  relevant features such as brightness, contrast, color balance, and sharpness. Outputs
  the resulting features.
input_from: ImageUploader
name: FeatureExtractor


## Transformer breakdown
- Decode the base64 image content to obtain the image
- Calculate the brightness of the image and multiply it with the brightness_scale
- Calculate the contrast of the image and multiply it with the contrast_scale
- Calculate the color balance of the image and multiply it with the color_balance_scale
- Calculate the sharpness of the image and multiply it with the sharpness_scale
- Create a dictionary with the calculated feature values
- Return the dictionary containing the image features

## Parameters
[{'name': 'brightness_scale', 'default_value': 1.0, 'description': 'The scaling factor for the brightness value.', 'type': 'float'}, {'name': 'contrast_scale', 'default_value': 1.0, 'description': 'The scaling factor for the contrast value.', 'type': 'float'}, {'name': 'color_balance_scale', 'default_value': 1.0, 'description': 'The scaling factor for the color balance value.', 'type': 'float'}, {'name': 'sharpness_scale', 'default_value': 1.0, 'description': 'The scaling factor for the sharpness value.', 'type': 'float'}]

        