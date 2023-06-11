from PIL import Image
import os
from typing import List

ORG_IMG = "./org"
DEST_IMG = "./dest"

BORDER_RATIO = 0.05

def load_images(path: str):
    images: List[Image.Image] = []

    for filename in os.listdir(path):
        img = Image.open(f"{path}/{filename}")
        images.append(img)
    return images

def save_images(images: List[Image.Image], path: str):
    for i in range(len(images)):
        images[i].save(f"{path}/{i}.png")

def squarify(img: Image.Image):
    old_size = img.size

    new_size = (round(max(old_size)*(1 + BORDER_RATIO)),round(max(old_size)*(1 + BORDER_RATIO)))
    new_img = Image.new("RGB", new_size, "White")
    box = tuple((n - o) // 2 for n, o in zip(new_size, old_size))
    new_img.paste(img, box)

    return new_img

if __name__=="__main__":
    images = load_images(ORG_IMG)
    images = [squarify(img) for img in images]
    save_images(images, DEST_IMG)
    