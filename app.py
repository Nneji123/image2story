import io
import os
import sys
import time

import cv2
import numpy as np
from prefix_clip import download_pretrained_model, generate_caption
from gpt2_story_gen import generate_story
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import PlainTextResponse
from PIL import Image
from pydantic import BaseModel
import warnings
warnings.filterwarnings("ignore")

sys.path.append(os.path.abspath(os.path.join("..", "config")))


app = FastAPI(
    title="Image2Story API",
    description="""An API for creating stories from an input image.""",
)


@app.get("/", response_class=PlainTextResponse, tags=["home"])
async def home():
    note = """
    Image2Story API 📚
    Note: add "/redoc" to get the complete documentation.
    """
    return note

@app.get("/username", response_class=PlainTextResponse, tags=["home"])
async def get_username(username: str):
    
    return username

class GenerateStory(BaseModel):
    model: str
    genre: str
    n_stories: int
    use_beam_search: bool

    class Config:
        schema_extra = {
            "example": {
                "model" : "coco",
                "genre": "superhero",
                "n_stories" :1,
                "use_beam_search":False
            }
        }


class GenerateCaption(BaseModel):
    model: str
    use_beam_search: bool

    class Config:
        schema_extra = {
            "example": {
                "model" : "coco",
                "use_beam_search":False
            }
        }

coco_weights = 'coco_weights.pt'
conceptual_weights = 'conceptual_weights.pt'


@app.post("/upload-and-save-image/{username}")
async def upload_save_image(username:str, file: UploadFile = File(...)):
    contents = io.BytesIO(await file.read())
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    try:
        os.makedirs(str(username))
        cv2.imwrite(f"./{username}/image.jpg", img)
        return "Upload Successful!"
    except FileExistsError as e:
        cv2.imwrite(f"./{username}/image.jpg", img)
        return "Upload Successful!"


@app.post("/generate-caption/{username}", response_class=PlainTextResponse, description="You can select the genre e.g sci_fi, action, drama, horror, thriller. Models: coco, conceptual")
async def generate_cap(username:str, data: GenerateCaption):
    try:
        if data.model.lower()=='coco':
            model_file = coco_weights
        elif data.model.lower()=='conceptual':
            model_file = conceptual_weights
        pil_image = Image.open(f"./{username}/image.jpg")
        image_caption = generate_caption(
            model_path=model_file,
            pil_image=pil_image,
            use_beam_search=data.use_beam_search,
        )
        story = image_caption
        time.sleep(1)
        os.system(f"rm -rf {username}")
        return story
    except FileNotFoundError as e:
        return "Please upload an image!"



@app.post("/generate-story/{username}", response_class=PlainTextResponse, description="You can select the genre e.g sci_fi, action, drama, horror, thriller. Models: coco, conceptual")
async def generate_storys(username:str, data: GenerateStory):
    try:
        if data.model.lower()=='coco':
            model_file = coco_weights
        elif data.model.lower()=='conceptual':
            model_file = conceptual_weights
        pil_image = Image.open(f"./{username}/image.jpg")
        image_caption = generate_caption(
            model_path=model_file,
            pil_image=pil_image,
            use_beam_search=data.use_beam_search,
        )
        story = generate_story(image_caption, pil_image, data.genre.lower(), data.n_stories)
        time.sleep(1)
        os.system(f"rm -rf {username}")
        return story
    except FileNotFoundError as e:
        return "Please upload an image!"


# import resource
# import platform
# import sys

# def memory_limit(percentage: float):
#     """
#     只在linux操作系统起作用
#     """
#     if platform.system() != "Linux":
#         print('Only works on linux!')
#         return
#     soft, hard = resource.getrlimit(resource.RLIMIT_AS)
#     resource.setrlimit(resource.RLIMIT_AS, (get_memory() * 1024 * percentage, hard))

# def get_memory():
#     with open('/proc/meminfo', 'r') as mem:
#         free_memory = 0
#         for i in mem:
#             sline = i.split()
#             if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
#                 free_memory += int(sline[1])
#     return free_memory

# def memory(percentage=0.8):
#     def decorator(function):
#         def wrapper(*args, **kwargs):
#             memory_limit(percentage)
#             try:
#                 return function(*args, **kwargs)
#             except MemoryError:
#                 mem = get_memory() / 1024 /1024
#                 print('Remain: %.2f GB' % mem)
#                 sys.stderr.write('\n\nERROR: Memory Exception\n')
#                 sys.exit(1)
#         return wrapper
#     return decorator

# @memory(percentage=0.80)
# def main():
#     print(f'My memory is limited to 80%.')

# main()