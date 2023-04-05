
# ComparisonPresenter

Presents a side-by-side comparison of the original and enhanced images, along with the specific edits applied. Outputs an edit summary.

## Initial generation prompt
description: Presents a side-by-side comparison of the original and enhanced images,
  along with the specific edits applied. Outputs an edit summary.
input_from: ImageEditor
name: ComparisonPresenter


## Transformer breakdown
- Load the original and edited Image objects
- Create a new blank Image of double width and same height as the inputs
- Paste the original and edited images side-by-side on the new blank Image
- Add labels for the original and edited images
- Create an edit summary string with the list of edits applied
- Output the combined comparison Image and the edit summary string

## Parameters
[]

        