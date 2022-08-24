from prefix_clip import download_pretrained_model, generate_caption
from gpt2_story_gen import generate_story

coco_weights = 'coco_weights.pt'
conceptual_weights = 'conceptual_weights.pt'
download_pretrained_model('coco', file_to_save=coco_weights)
download_pretrained_model('conceptual', file_to_save=conceptual_weights)

