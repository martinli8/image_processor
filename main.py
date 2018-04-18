from pymodm import connect
import models
import datetime
from skimage import data, img_as_float, io, exposure
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
    return user.process_duration

def histogram_eq():
    pass


def contrast_stretching():
    pass


def log_compression():
    img = data.moon()
    img_c = img
    max_val = numpy.amin(img)
    for x in numpy.nditer(img_c, op_flags=['readwrite']):
        x[...] = numpy.log10(1+x)
    print(img)
    print(img_c)
    img_plot_2 = plt.imshow(img_c)
    plt.show()
    pass


def reverse_video():
    pass


def other():
    pass

if __name__ == '__main__':
    log_compression()