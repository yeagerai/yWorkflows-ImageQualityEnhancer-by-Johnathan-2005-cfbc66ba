
import os
import base64
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from core.abstract_component import AbstractComponent


class ImageUploaderInputDict(BaseModel):
    image: UploadFile


class ImageUploaderOutputDict(BaseModel):
    filename: str
    content_base64: str
    file_format: str


class ImageUploader(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()

    def transform(
        self, args: ImageUploaderInputDict
    ) -> ImageUploaderOutputDict:
        print(f"Executing the transform of the {type(self).__name__} component...")

        file_format = args.image.filename.split(".")[-1].lower()
        supported_formats = ["jpg", "jpeg", "png", "gif"]

        if file_format not in supported_formats:
            raise ValueError("Unsupported file format")

        content_base64 = base64.b64encode(args.image.file.read()).decode("utf-8")

        return ImageUploaderOutputDict(
            filename=args.image.filename,
            content_base64=content_base64,
            file_format=file_format,
        )


image_uploader_app = FastAPI()


@image_uploader_app.post("/transform/")
async def transform(
    args: UploadFile = File(...),
) -> ImageUploaderOutputDict:
    image_uploader = ImageUploader()
    return image_uploader.transform(args=ImageUploaderInputDict(image=args))

