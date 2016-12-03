import argparse
import os
from PIL import Image
from collections import OrderedDict


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


def make_resize_and_check_logic(image, scale, height, width, name, output):
        is_logic_right = 0
        if height and not scale and not width:
            image = resize_by_height_only(image, float(height))
            is_logic_right = 1
        if width and not scale and not height:
            image = resize_by_width_only(image, float(width))
            is_logic_right = 1
        if scale and not width and not height:
            image = resize_by_scale_only(image, float(scale))
            is_logic_right = 1
        if width and height and not scale:
            image = resize_by_height_and_width(image, float(width), float(height))
            is_logic_right = 1
        return is_logic_right, image


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
    args_dict = OrderedDict((
        ("scale", args["scale"]),
        ("height", args["height"]),
        ("width", args["width"]),
        ("name", args["name"]),
        ("output", args["output"]),
    ))
    return args_dict


def save_image(full_path, output_folder_name):
    try:
        image.save(full_path)
    except:
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
    resized_image_name = get_image_name(name, resized_image).split('/')[-1]
    if not output:
        if '/' not in name:
            return resized_image_name
        else:
            return '/'.join(['/'.join(name.split('/')[:-1]), resized_image_name])
    else:
        return '/'.join([output.rstrip('/'), resized_image_name])

    
if __name__ == '__main__':
    args_dict = parse_args()
    image = Image.open(args_dict["name"])
    is_logic_right, resized_image = make_resize_and_check_logic(image, *args_dict.values())
    if not is_logic_right:
        explain_user_about_wrong_logic(**args_dict)
    full_path = get_full_image_path(resized_image, args_dict["output"], args_dict["name"])
    save_image(full_path, args_dict["output"])
