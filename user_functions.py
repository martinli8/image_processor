import models
import datetime
import base64
from image_functions import imageSize
import test_image_processing


def save_filename_base64(user_email, fileName, base64result):
    """
    Saves the filename as well as the base64 string to the user class
    :param user_email: Primary key that user is saved under
    :param fileName: Name of the file that is saved
    :param base64result: The base64 string of the user
    """

    user = models.User.objects.raw({"_id": user_email}).first()
    user.processed_image_name.append(fileName)
    user.processed_image_string.append(base64result)
    user.save()


def create_user(email, picture, p_req, upload_time):
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

    u = models.User(email, [], [], [], [], [], [], [])
    u.picture.append(picture)
    u.process_requested.append(p_req)
    u.upload_time.append(upload_time)
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

def write_image_size(user_email, image_size):
    """
    Determines the uploaded image size and saves it
    :param user_email: The primary key used to open up the user
    :param process_duration: List containing the
    """

    user = models.User.objects.raw({"_id": user_email}).first()
    user.image_size.append(image_size)
    user.save()
    return user.image_size


def add_user_data(email, picture, p_req, upload_time):
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
    u.image_size.append(imageSize(test_image_processing.image_string))
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
        "process_duration": user.process_duration,
    }
    return data


def save_image(user_email, image_string, status):
    """
    Saves the image to disk
    :param user_email: Primary key that user is saved under
    :param image_string: Base-64 image string to save file to
    :return imageName: name of the image that was saved to disk
    """

    user = models.User.objects.raw({"_id": user_email}).first()
    user_short = user_email.split('@')[0]
    picture_idx = len(user.process_requested)
    if status is "PRE":
        imageName = user_short + "_pre_" + str(picture_idx) + ".png"
    if status is "POST":
        imageName = user_short + "_post_" + str(picture_idx) + ".png"
    fh = open(imageName, "wb")
    fh.write(base64.b64decode(image_string))
    fh.close()
    return imageName
