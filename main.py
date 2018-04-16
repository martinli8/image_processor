from pymodm import connect
import models
import datetime
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


def histogram_eq():
    pass


def contrast_stretching():
    pass


def log_compression():
    pass


def reverse_video():
    pass


def other():
    pass
