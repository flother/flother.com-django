from PIL.Image import ANTIALIAS


def create_thumbnail(im, size, image_filter=ANTIALIAS):
    """
    Modify the given image to be a thumbnail of exactly the size given.
    This is different to the built-in im.thumbnail() method, which only
    approximates the thumbnail size.
    """
    input_image_size = float(im.size[0]), float(im.size[1])
    input_aspect_ratio = input_image_size[0] / input_image_size[1]
    output_aspect_ratio = float(size[0]) / float(size[1])

    # Work out what to crop to fit the image into the new dimensions.
    if input_aspect_ratio >= output_aspect_ratio:
        # Input image is wider than required; crop the sides.
        crop_width = int(output_aspect_ratio * input_image_size[1] + 0.5)
        crop_height = int(input_image_size[1])
    else:
        # Input image taller than required; crop the top and bottom.
        crop_width = int(input_image_size[0])
        crop_height = int(input_image_size[0] / output_aspect_ratio + 0.5)

    # Crop the image.
    left_side = int((input_image_size[0] - crop_width) * 0.50)
    if left_side < 0:
        left_side = 0
    top_side = int((input_image_size[1] - crop_height) * 0.50)
    if top_side < 0:
        top_side = 0
    output_image = im.crop((left_side, top_side, left_side + crop_width,
        top_side + crop_height))

    return output_image.resize(size, image_filter)
