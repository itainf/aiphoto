from pymatting import *
from PIL import Image

colour_dict = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "blue": (67, 142, 219)
}


def to_background(org, resize_trimap, id_image, colour):
    """
        org：原始图片
        resize_trimap：trimap
        id_image：新图片
        colour: 背景颜色
    """
    scale = 1.0
    image = load_image(org, "RGB", scale, "box")
    trimap = load_image(resize_trimap, "GRAY", scale, "nearest")
    im = Image.open(org)
    # estimate alpha from image and trimap
    alpha = estimate_alpha_cf(image, trimap)

    new_background = Image.new('RGB', im.size, colour_dict[colour])
    new_background.save("bj.png")
    # load new background
    new_background = load_image("bj.png", "RGB", scale, "box")


    # estimate foreground from image and alpha
    foreground, background = estimate_foreground_ml(image, alpha, return_background=True)

    # blend foreground with background and alpha
    new_image = blend(foreground, new_background, alpha)
    save_image(id_image, new_image)


def to_background_grid(org, resize_trimap, id_image):
    """
        org：原始图片
        resize_trimap：trimap
        id_image：新图片
        colour: 背景颜色
    """
    scale = 1.0
    image = load_image(org, "RGB", scale, "box")
    trimap = load_image(resize_trimap, "GRAY", scale, "nearest")
    im = Image.open(org)
    # estimate alpha from image and trimap
    alpha = estimate_alpha_cf(image, trimap)

    # estimate foreground from image and alpha
    foreground, background = estimate_foreground_ml(image, alpha, return_background=True)
    images = [image]
    for k,v in colour_dict.items():
        new_background = Image.new('RGB', im.size, v)
        new_background.save("bj.png")
        new_background = load_image("bj.png", "RGB", scale, "box")
        new_image = blend(foreground, new_background, alpha)
        images.append(new_image)

    grid = make_grid(images)
    save_image(id_image, grid)

