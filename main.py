from pymodm import connect
import models
import datetime
import numpy
import base64
from PIL import Image
from skimage import exposure, filters
from skimage import io

connect("mongodb://vcm-3590.vm.duke.edu:27017/image_processor")


def create_user(email, picture, p_req, upload_time, size):
    """
    Creates a user with the specified paramters. If the user already exists
    in the DB this WILL overwite the user. Also adds specified data regarding
    what the user requested. All user actions are tied to an email primary key,
    necessitating a list to save the data assosciated with each user's actions.

    :param email: str email of the new User
    :param picture: 64bit- string representation of picture
    :param p_req: Image processing technique requested on picture (Contrast
    stretching, histogram equalization, Log compression, etc.)
    :param p_dur: Latency in processing not sure which one yet
    :param upload_time: Time it takes to upload the image
    :param image_size: Pixel x Pixel size of the image, stored in a tuple
    """

    u = models.User(email, [], [], [], [], [])
    u.picture.append(picture)
    u.process_requested.append(p_req)
    u.upload_time.append(upload_time)
    u.image_size.append(size)
    u.save()


def write_duration_time(user_email, process_duration):
    """
    Updates the user duration and saves it
    :param user_email: The primary key used to open up the user
    :param process_duration: The process duration to save it to the User model
    """

    user = models.User.objects.raw({"_id": user_email}).first()
    user.process_duration.append(process_duration)
    user.save()
    return user.process_duration


def add_user_data(email, picture, p_req, upload_time, size):
    """
    Appends user data to the existing user with email primary key
    :param email: Primary key for the user
    :param picture: Base-64 representation of user uploaded picture
    :param p_req: Process requested by the user (Ex. Hist. eq)
    :param upload_time: Time it took to upload the file from the user end
    :param size: Size of the uploaded image
    """

    u = models.User.objects.raw({"_id": email}).first()
    u.picture.append(picture)
    u.process_requested.append(p_req)
    u.upload_time.append(upload_time)
    u.image_size.append(size)
    u.save()


def return_metadata(email):
    """
    Returns user metadata regarding relevant uploads in a dict
    :param email: Primary key for the user requesting metadata
    :return data: A dict of the user metadata
    """

    user = models.User.objects.raw({"_id": email}).first()
    data = {
        "user_email": user.email,
        "pictures": user.picture,
        "process_requested": user.process_requested,
        "upload_time": user.upload_time,
        "image_size": user.image_size,
        "process_duration": user.process_duration
    }
    return data


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

    if process_requested is "histogram_eq":
        timeNow = datetime.datetime.now()
        imageResult = histogram_eq(decoded_image)

    if process_requested is "contrast_stretching":
        timeNow = datetime.datetime.now()
        imageResult = contrast_stretch(decoded_image)

    if process_requested is "log_compression":
        timeNow = datetime.datetime.now()
        imageResult = log_compression(decoded_image)

    if process_requested is "reverse_video":
        timeNow = datetime.datetime.now()
        imageResult = reverse_video(decoded_image)

    if process_requested is "edge_detection":
        timeNow = datetime.datetime.now()
        imageResult = edge_detection(decoded_image)

    timePostProcessing = datetime.datetime.now()
    process_duration = (timePostProcessing - timeNow).total_seconds()
    write_duration_time(user_email, process_duration)

    base64result = encodeImage(imageResult)
    # save_processed_image(user_email, base64result)

    return base64result


def histogram_eq(img):
    """
    Function takes in an image and performs histogram equalization

    :param img: Is a uint8 array
    :return img_eq: Is a uint8 array after histogram equalization
    """
    img_eq = exposure.equalize_hist(img.astype('uint8'))
    img_eq = 255*img_eq
    return img_eq.astype('uint8')


def contrast_stretch(img):
    """
    Function takes in an image and performs contrast contrast_stretching

    :param img: Is a uint8 array
    :return img_rescale: Is a uint8 array after contrast stretching
    """
    p2, p98 = numpy.percentile(img, (2, 98))
    img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))
    return img_rescale.astype('uint8')


def log_compression(img):
    """
    Function will take in an image and perform log compression.
    :param img: Is a uint8 array image
    :param image_log: Is a unit8 array image that was log compressed
    """
    image_log = numpy.copy(img.astype('uint8'))
    for x in numpy.nditer(image_log, op_flags=['readwrite']):
        x[...] = numpy.log10(1+x)
    return image_log


def reverse_video(img):
    """
    Takes in an image and reverses the colors in the image by
    subtracting the pixel value from 225.
    :param img: A uint8 2D array of the image that will undergo the opperation
    :return image_reverse: A uint8 2D array of image with pixels inverted.
    """
    image_reverse = numpy.copy(img.astype('uint8'))
    for x in numpy.nditer(image_reverse, op_flags=['readwrite']):
        x[...] = 255 - x
    return image_reverse.astype('uint8')


def edge_detection(img):
    """
    Function detects the edges of a 2D array grayscale image using
    the sobel filter and returns an image containing the edges.
    :param img: Image, 2D grayscale array, on which edge detection
    will be performed
    :return edges: Edges is a uint8 array that contians the edges
    found through sobel filtering
    """
    edges = filters.sobel(img)
    return edges.astype('uint8')


def decodeImage(image_string):
    """
    Function will take in a base64 string and reconstructed into an image
    :param image_string: 64bit- string representation of picture
    :return img_read: reconstructed image as PIL Image object
    """
    fh = open("temp.png", "wb")
    fh.write(base64.b64decode(image_string))
    fh.close()
    img = base64.b64decode(image_string)
    img_read = io.imread("temp.png")
    return img_read


def encodeImage(data_array):
    """
    Function will take in a data-type returned from the data processing method
    to a base 64 image to be returned to the front-end
    :param img: Unit-8 array
    :return :
    """
    print(type(data_array))
    encoded_image_string = base64.b64encode(data_array)
    return encoded_image_string


def save_image(user_email, image_string, status):
    """
    Saves the image as well as the file path to the user class
    :param user_email: Primary key that user is saved under
    :param image_string: Base-64 image string to save file to
    """

    user = models.User.objects.raw({"_id": user_email}).first()
    picture_idx = len(user.process_requested)
    if status is "PRE":
        imageName = user_email + "pre" + str(picture_idx) + ".png"
    if status is "POST":
        imageName = user_email + "post" + str(picture_idx) + ".png"
    fh = open(imageName, "wb")
    fh.write(base64.b64decode(image_string))
    fh.close()
