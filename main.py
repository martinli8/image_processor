from pymodm import connect
import models
import datetime
import numpy as np
from skimage import data, img_as_float, io, exposure

connect("mongodb://vcm-3590.vm.duke.edu:27017/image_processor")

def create_user(email, picture, p_req, p_dur, upload_time, size):
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
    u.process_duration.append(p_dur)
    u.upload_time.append(upload_time)
    u.image_size.append(size)
    u.save()


def histogram_eq(img):
    """
    Function takes in an image and performs histogram equalization

    :param img: Is a uint8 array
    :return img_eq: Is a uint8 array after histogram equalization
    """
    img_eq = exposure.equalize_hist(img)
    return img_eq.astype('uint8')


def contrast_stretching(img):
    """
    Function takes in an image and performs contrast contrast_stretching

    :param img: Is a uint8 array
    :return img_rescale: Is a uint8 array after contrast stretching
    """
    p2, p98 = np.percentile(img, (2, 98))
    img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))
    return img_rescale.astype('uint8')


def log_compression():
    pass


def reverse_video():
    pass


def other():
    pass
