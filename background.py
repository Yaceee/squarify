from enum import Enum
from PIL import Image, ImageStat, ImageFilter, ImageChops

class BACKGROUND_TYPE(Enum):
    WHITE = 1
    BLACK = 2
    AVERAGE = 3
    AVERAGE_DROPSHADOW = 4
    AMBILIGHT = 5
    SYNTHWAVE = 6
    GRADIENT = 7
    MEDIAN = 8

def background_white(size: tuple, img: Image.Image):
    background = Image.new("RGB", size, "White")
    return background

def background_black(size: tuple, img: Image.Image):
    background = Image.new("RGB", size, "Black")
    return background

def background_average(size: tuple, img: Image.Image):
    stat = ImageStat.Stat(img)
    average = tuple([ round(m) for m in stat.mean])
    background = Image.new("RGB", size, average)
    return background

def background_median(size: tuple, img: Image.Image):
    stat = ImageStat.Stat(img)
    average = tuple([ round(m) for m in stat.median])
    background = Image.new("RGB", size, average)
    return background

def background_average_dropshadow(size: tuple, img: Image.Image):
    radius_ratio = 0.5
    box = tuple((n - o) // 2 for n, o in zip(size, img.size))
    stat = ImageStat.Stat(img)
    radius = ( round(radius_ratio*(size[0]-img.size[0])), round(radius_ratio*(size[1]-img.size[1])))

    average = tuple([ round(m) for m in stat.mean])
    background = Image.new("RGB", size, "White")
    box_img = Image.new("RGB", img.size, average)
    background.paste(box_img, box)
    return background.filter(filter=ImageFilter.GaussianBlur(min(radius)))

def background_ambilight(size: tuple, img: Image.Image):
    radius_ratio = 0.4
    box = tuple((n - o) // 2 for n, o in zip(size, img.size))
    radius = ( round(radius_ratio*(size[0]-img.size[0])), round(radius_ratio*(size[1]-img.size[1])))

    background = Image.new("RGB", size, "White")
    img_hsv = img.copy().convert('HSV')
    ambi_v = ImageChops.constant(img_hsv.getchannel(2), 255)
    ambi_hsv = Image.merge("HSV", [img_hsv.getchannel(0), img_hsv.getchannel(1), ambi_v])
    ambi = ambi_hsv.convert("RGB")
    background.paste(ambi, box)
    return background.filter(filter=ImageFilter.GaussianBlur(min(radius)))

def background_synthwave(size: tuple, img: Image.Image):
    radius_ratio = 1
    box = tuple((n - o) // 2 for n, o in zip(size, img.size))
    radius = ( round(radius_ratio*(size[0]-img.size[0])), round(radius_ratio*(size[1]-img.size[1])))

    background = Image.new("RGB", size, "White")
    img_hsv = img.copy().convert('HSV')
    ambi_v = ImageChops.constant(img_hsv.getchannel(2), 255)
    ambi_hsv = Image.merge("HSV", [img_hsv.getchannel(0), img_hsv.getchannel(1), ambi_v])
    ambi = ambi_hsv.convert("RGB")
    background.paste(ambi, box)

    ambi_hsv_blur = background.filter(filter=ImageFilter.GaussianBlur(radius)).convert('HSV')
    grad_v = ImageChops.constant(ambi_hsv_blur.getchannel(2), 255)
    grad_s = ImageChops.constant(ambi_hsv_blur.getchannel(1), 255)
    grad_hsv = Image.merge("HSV", [ambi_hsv_blur.getchannel(0), grad_s, grad_v])
    return grad_hsv.convert("RGB")

def background_gradient(size: tuple, img: Image.Image):
    radius_ratio = 1
    box = tuple((n - o) // 2 for n, o in zip(size, img.size))
    radius = ( round(radius_ratio*(size[0]-img.size[0])), round(radius_ratio*(size[1]-img.size[1])))

    background = Image.new("RGB", size, "White")
    img_hsv = img.copy().convert('HSV')
    ambi_v = ImageChops.constant(img_hsv.getchannel(2), 255)
    ambi_hsv = Image.merge("HSV", [img_hsv.getchannel(0), img_hsv.getchannel(1), ambi_v])
    ambi = ambi_hsv.convert("RGB")
    background.paste(ambi, box)

    ambi_hsv_blur = background.filter(filter=ImageFilter.GaussianBlur(radius)).convert('HSV')
    grad_v = ImageChops.constant(ambi_hsv_blur.getchannel(2), 255)
    grad_hsv = Image.merge("HSV", [ambi_hsv_blur.getchannel(0), ambi_hsv_blur.getchannel(1), grad_v])
    return grad_hsv.convert("RGB")


def get_background_function(type: BACKGROUND_TYPE):
    match type:
        case BACKGROUND_TYPE.WHITE:
            return background_white
        case BACKGROUND_TYPE.BLACK:
            return background_black
        case BACKGROUND_TYPE.AVERAGE:
            return background_average
        case BACKGROUND_TYPE.AVERAGE_DROPSHADOW:
            return background_average_dropshadow
        case BACKGROUND_TYPE.AMBILIGHT:
            return background_ambilight
        case BACKGROUND_TYPE.SYNTHWAVE:
            return background_synthwave
        case BACKGROUND_TYPE.GRADIENT:
            return background_gradient
        case BACKGROUND_TYPE.MEDIAN:
            return background_median

def get_background(size: tuple, img: Image.Image, type: BACKGROUND_TYPE):
    background_function = get_background_function(type)
    background = background_function(size, img)
    return background