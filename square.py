from typing import List
import os
from PIL import Image
import background

ORG_IMG = "./org"
DEST_IMG = "./dest"

BORDER_RATIO = 0.05
ASPECT_RATIO = 1
REDUCE_FACTOR = 2
BACKGROUND_TYPE = background.BACKGROUND_TYPE.AVERAGE_DROPSHADOW

def load_images(path: str):
    images: List[Image.Image] = []

    for filename in os.listdir(path):
        if(filename != ".DS_Store"):
            img = Image.open(f"{path}/{filename}")
            images.append(img)
    return images

def save_images(images: List[Image.Image], path: str):
    for i in range(len(images)):
        images[i].save(f"{path}/{i}.png")

def squarify(img: Image.Image):
    old_size = img.size

    aspect_multiplicator = ASPECT_RATIO if old_size[0] < old_size[1] else 1/ASPECT_RATIO

    new_size = (round(max(old_size)*(1 + BORDER_RATIO)*min(aspect_multiplicator, 1)),round(max(old_size)*(1 + BORDER_RATIO)*max(aspect_multiplicator, 1)))
    new_img = background.get_background(new_size, img, BACKGROUND_TYPE)
    box = tuple((n - o) // 2 for n, o in zip(new_size, old_size))
    new_img.paste(img, box)

    return new_img.reduce(REDUCE_FACTOR)

if __name__=="__main__":
    images = load_images(ORG_IMG)
    images = [squarify(img) for img in images]
    save_images(images, DEST_IMG)
    