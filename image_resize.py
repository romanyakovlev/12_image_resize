import argparse
import os
from PIL import Image


def resize_by_height_only(image, height):
    original_width, original_height = image.size
    resize_coef = height / original_height
    resized_width = original_width * resize_coef
    resized_height = original_height * resize_coef
    resized_image = image.resize((int(resized_width), int(resized_height)))
    return resized_image


def resize_by_width_only(image, width):
    original_width, original_height = image.size
    resize_coef = width / original_width
    resized_width = original_width * resize_coef
    resized_height = original_height * resize_coef
    resized_image = image.resize((int(resized_width), int(resized_height)))
    return resized_image


def resize_by_height_and_width(image, width, height):
    original_width, original_height = image.size
    resized_image = image.resize((int(width), int(height)))
    return resized_image


def resize_by_scale_only(image, scale):
    original_width, original_height = image.size
    scaled_width = original_width * scale
    scaled_height = original_height * scale
    resized_image = image.resize((int(scaled_width), int(scaled_height)))
    return resized_image


def make_resize(image, scale, height, width, name, output):
    is_logic_right = False
    if height and not scale and not width:
        image = resize_by_height_only(image, float(height))
        is_logic_right = True
    if width and not scale and not height:
        image = resize_by_width_only(image, float(width))
        is_logic_right = True
    if scale and not width and not height:
        image = resize_by_scale_only(image, float(scale))
        is_logic_right = True
    if width and height and not scale:
        image = resize_by_height_and_width(image, float(width), float(height))
        is_logic_right = True
    return is_logic_right, image


def check_logic(scale, height, width, name, output):
    is_logic_right = False
    if height and not scale and not width:
        is_logic_right = True
    if width and not scale and not height:
        is_logic_right = True
    if scale and not width and not height:
        is_logic_right = True
    if width and height and not scale:
        is_logic_right = True
    return is_logic_right

def get_image_name(original_name, image):
    full_image_name = os.path.splitext(original_name)
    image_name, image_width = full_image_name[0], str(image.width)
    image_height, image_format = str(image.height), full_image_name[1]
    resized_name = "{}__{}x{}{}".format(image_name, image_width, image_height, image_format)
    return resized_name


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width')
    parser.add_argument('--height')
    parser.add_argument('--scale')
    parser.add_argument('--output')
    parser.add_argument('name')
    args = vars(parser.parse_args())
    return args


def save_image(full_path, output_folder_name):
    try:
        image.save(full_path)
    except FileNotFoundError:
        print("'{}' folder does not exist. We create it and place your resized image inside".format(
              output_folder_name))
        os.makedirs(output_folder_name)
        image.save(full_path)
    print("Success! Your file in '{}'.".format(full_path))


def explain_user_about_wrong_logic(**resize_arguments):
    print("Oops! You make a mistake in the choice of arguments. There is arguments you choose:\n")
    for key,value in resize_arguments.items():
        print(key, 'yes' if value else 'no')
    print("\nIt's not right combination of arguments. You can choose these combinations:\n\n-scale only"
          "\n-widht and height\n-height/width only\n")
    quit()


def get_full_image_path(resized_image, output, name):
    os_sep = os.sep
    resized_image_name = get_image_name(name, resized_image).split(os_sep)[-1]
    if not output:
        if os_sep not in name:
            return resized_image_name
        else:
            return os_sep.join([os_sep.join(name.split(os_sep)[:-1]), resized_image_name])
    else:
        return os_sep.join([output.rstrip(os_sep), resized_image_name])


if __name__ == '__main__':
    args = parse_args()
    scale, height, width, name, output = [args["scale"], args["height"], args["width"],
                                          args["name"], args["output"]]
    image = Image.open(name)
    resized_image = make_resize(image, scale, height, width, name, output)
    is_logic_right = check_logic(scale, height, width, name, output)
    if not is_logic_right:
        explain_user_about_wrong_logic(**args)
    full_path = get_full_image_path(resized_image, output, name)
    save_image(full_path, output)
