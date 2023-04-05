
import os
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
from core.abstract_component import AbstractComponent

class ComparisonPresenterInputDict(BaseModel):
    original_image: bytes
    edited_image: bytes
    edits: List[str]

class ComparisonPresenterOutputDict(BaseModel):
    comparison_image: bytes
    edit_summary: str

class ComparisonPresenter(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()

    def transform(
        self, args: ComparisonPresenterInputDict
    ) -> ComparisonPresenterOutputDict:

        # Load the original and edited Image objects
        original_image = Image.open(BytesIO(args.original_image))
        edited_image = Image.open(BytesIO(args.edited_image))

        # Create a new blank Image of double width and same height as the inputs
        width, height = original_image.size
        new_width = 2 * width
        comparison_image = Image.new("RGB", (new_width, height))

        # Paste the original and edited images side-by-side on the new blank Image
        comparison_image.paste(original_image, (0, 0))
        comparison_image.paste(edited_image, (width, 0))

        # Add labels for the original and edited images
        # Please note that you may need to install additional image processing
        # libraries to add labels to the images (e.g., PIL, OpenCV)

        # Create an edit summary string with the list of edits applied
        edit_summary = "Edits applied: " + ", ".join(args.edits)

        # Output the combined comparison Image and the edit summary string
        buffered = BytesIO()
        comparison_image.save(buffered, format="PNG")
        comparison_bytes = buffered.getvalue()

        out = ComparisonPresenterOutputDict(
            comparison_image=comparison_bytes,
            edit_summary=edit_summary
        )
        return out


comparison_presenter_app = FastAPI()

@comparison_presenter_app.post("/transform/")
async def transform(
    args: ComparisonPresenterInputDict,
) -> ComparisonPresenterOutputDict:
    comparison_presenter = ComparisonPresenter()
    return comparison_presenter.transform(args)
