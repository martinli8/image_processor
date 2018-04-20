from pymodm import connect
import models
import datetime
import numpy
import base64
from PIL import Image
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


def histogram_eq():
    pass


def contrast_stretching():
    pass


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
    img_read = Image.open("temp.png")
    return img_read
