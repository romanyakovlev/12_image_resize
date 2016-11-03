import argparse
from PIL import Image
import os


def height_only(image, height):
    original_width, original_height = image.size
    resize_coef = height / original_height
    resized_width = original_width * resize_coef
    resized_height = original_height * resize_coef
    resized_image = image.resize((int(resized_width), int(resized_height)))
    return resized_image


def width_only(image, width):
    original_width, original_height = image.size
    resize_coef = width / original_width
    resized_width = original_width * resize_coef
    resized_height = original_height * resize_coef
    resized_image = image.resize((int(resized_width), int(resized_height)))
    return resized_image


def height_and_width(image, width, height):
    original_width, original_height = image.size
    resized_image = image.resize((int(width), int(height)))
    return resized_image


def scale_only(image, scale):
    original_width, original_height = image.size
    scaled_width = original_width * scale
    scaled_height = original_height * scale
    resized_image = image.resize((int(scaled_width), int(scaled_height)))
    return resized_image


def get_resize_type(image, scale, height, width, name, output):
        is_logic_right = 0
        if height and not scale and not width:
            image = height_only(image, float(height))
            is_logic_right = 1
        if width and not scale and not height:
            image = width_only(image, float(width))
            is_logic_right = 1
        if scale and not width and not height:
            image = scale_only(image, float(scale))
            is_logic_right = 1
        if width and height and not scale:
            image = height_and_width(image, float(width), float(height))
            is_logic_right = 1
        return is_logic_right, image


def get_image_name(name, image):
    image_name = os.path.splitext(name)
    image_name = image_name[0] + '__' + str(image.width) + 'x' + str(image.height) + image_name[1]
    return image_name


def get_image_path(resized_image_name, output, name):
    if not output:
        if '/' not in name:
            return resized_image_name
        else:
            return '/'.join(['/'.join(name.split('/')[:-1]), resized_image_name])
    else:
        return '/'.join([output.rstrip('/'), resized_image_name])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--width')
    parser.add_argument('--height')
    parser.add_argument('--scale')
    parser.add_argument('--output')
    parser.add_argument('name')
    args = vars(parser.parse_args())
    scale, height, width, name, output = [
        args["scale"],
        args["height"],
        args["width"],
        args["name"],
        args["output"],
    ]
    image = Image.open(name)
    is_logic_right, resized_image = get_resize_type(image, scale, height, width, name, output)
    if not is_logic_right:  print('You do something wrong. Set another arguments.')
    resized_image_name = get_image_name(name, resized_image).split('/')[-1]
    full_path = get_image_path(resized_image_name, output, name)
    try:
        image.save(full_path)
    except:
        print("'{}' folder does not exist. We create it and place your resized image inside".format(output))
        os.makedirs(output)
        image.save(full_path)
    print("Success! Your file is '{}'.".format(resized_image_name))
