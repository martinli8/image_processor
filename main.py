from pymodm import connect
import models
import datetime
from skimage import data, img_as_float, io, exposure, filters
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy
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
    """
    u = models.User.objects.raw({"_id": email}).first()
    u.picture.append(picture)
    u.process_requested.append(p_req)
    u.upload_time.append(upload_time)
    u.image_size.append(size)
    u.save()


def return_metadata(email):
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


def log_compression():
    pass


def reverse_video():
    pass


def edge_detection(img):
    """
    Function detects the edges of a 2D array grayscale image using the sobel filter
    and returns an image containing the edges. 
    :param img: Image, 2D grayscale array, on which edge detection will be performed
    :return edges: Edges is a uint8 array that contians the edges found through sobel filtering
    """
    edges = filters.sobel(img)
    return edges.astype('uint8')
