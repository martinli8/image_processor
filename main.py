from pymodm import connect
from image_functions import *
from user_functions import *


connect("mongodb://vcm-3590.vm.duke.edu:27017/image_processor")


def process_image(user_email, process_requested, bituser_picture):
    """
    Takes in process_requested and base-64 picture, calls the appropriate
    image processing method, saves the time that it takes to process the image,
    and returns the result in a base64 image.
    :param user_email: Primary key that user is saved under
    :param process_requested: Image processing method requested on image
    :param bituser_picture: Base 64 representation of the user-uploaded image
    :return base64result: Base 64 represnetation of the processed image
    """

    decoded_image = decodeImage(bituser_picture)
    write_image_size(user_email, imageSize(bituser_picture))
    conversionFlag = False
    original_histogram = ""
    processed_histogram = ""

    if process_requested == "histogram_eq":
        if grayScaleDetection2(bituser_picture) is False:
            img = grayScaleConversion(bituser_picture)
            conversionFlag = True
            decoded_image = img
            original_histogram = calculate_histogram(img)
        timeNow = datetime.datetime.now()
        imageResult = histogram_eq(decoded_image)
        processed_histogram = calculate_histogram(imageResult)

    if process_requested == "contrast_stretching":
        timeNow = datetime.datetime.now()
        imageResult = contrast_stretch(decoded_image)

    if process_requested == "log_compression":
        timeNow = datetime.datetime.now()
        imageResult = log_compression(decoded_image)

    if process_requested == "reverse_video":
        timeNow = datetime.datetime.now()
        imageResult = reverse_video(decoded_image)

    if process_requested == "edge_detection":
        if grayScaleDetection2(bituser_picture) is False:
            img = grayScaleConversion(bituser_picture)
            conversionFlag = True
            decoded_image = img
        timeNow = datetime.datetime.now()
        imageResult = edge_detection(decoded_image)

    timePostProcessing = datetime.datetime.now()
    process_duration = (timePostProcessing - timeNow).total_seconds()
    write_duration_time(user_email, process_duration)

    base64result = encodeImage(imageResult)
    fileName = save_image(user_email, base64result, "POST")

    save_filename_base64(user_email, fileName, base64result)
    write_conversionFlag(user_email, conversionFlag)
    save_histogram_values(user_email, original_histogram, processed_histogram)


    return base64result
