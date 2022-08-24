import os

from prefix_clip import download_pretrained_model, generate_caption
from gpt2_story_gen import generate_story

if os.path.exists("coco_weights.pt"):
    pass
else:
    coco_weights = 'coco_weights.pt'
    conceptual_weights = 'conceptual_weights.pt'
    download_pretrained_model('coco', file_to_save=coco_weights)
    download_pretrained_model('conceptual', file_to_save=conceptual_weights)

def download_stuff():
    from PIL import Image
    pil_image = Image.open("image.jpg")
    model_file = 'coco_weights.pt'
    cap = generate_caption(model_path=model_file, pil_image=pil_image, use_beam_search=False)
    print(cap)

download_stuff()