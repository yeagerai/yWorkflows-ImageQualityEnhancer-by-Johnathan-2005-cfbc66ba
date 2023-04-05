
import typing
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.workflows.abstract_workflow import AbstractWorkflow


class UploadedImage(BaseModel):
    content: str
    filename: str
    format: str


class EnhancedImage(BaseModel):
    content: str
    edits_summary: List[str]
    filename: str
    format: str


class ImageQualityEnhancer(AbstractWorkflow):
    def __init__(self) -> None:
        super().__init__()

    async def transform(
        self, args: UploadedImage, callbacks: typing.Any
    ) -> EnhancedImage:
        results_dict = await super().transform(args=args, callbacks=callbacks)
        
        # Extract the results from the results_dict
        enhanced_image_content = results_dict[1].content
        performed_edits = results_dict[2].edits_summary
        enhanced_image_filename = results_dict[3].filename
        enhanced_image_format = results_dict[3].format
        
        out = EnhancedImage(
            content=enhanced_image_content,
            edits_summary=performed_edits,
            filename=enhanced_image_filename,
            format=enhanced_image_format,
        )
        return out

load_dotenv()
image_quality_enhancer_app = FastAPI()


@image_quality_enhancer_app.post("/transform/")
async def transform(
    args: UploadedImage,
) -> EnhancedImage:
    image_quality_enhancer = ImageQualityEnhancer()
    return await image_quality_enhancer.transform(args, callbacks=None)
