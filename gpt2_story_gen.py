from transformers import pipeline


def generate_story(image_caption, image, genre, n_stories):

    story_gen = pipeline(
        "text-generation", 
        "pranavpsv/genre-story-generator-v2"
        )
    
    input = f"<BOS> <{genre}> {image_caption}"
    stories = '\n\n'.join([f"Story {i+1}\n{story_gen(input)[0]['generated_text'].strip(input)}" for i in range(n_stories)])

    return stories
