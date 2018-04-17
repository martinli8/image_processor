from pymodm import connect
import models
import datetime
import matplotlib
import matplotlib.pyplot as plt
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


def plot_img_and_hist(image, axes, bins=256):
    """
    Plot an image along with its histogram and cumulative histogram.

    """
    image = img_as_float(image)
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()

    # Display image
    ax_img.imshow(image, cmap=plt.cm.gray)
    ax_img.set_axis_off()

    # Display histogram
    ax_hist.hist(image.ravel(), bins=bins, histtype='step', color='black')
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Pixel intensity')
    ax_hist.set_xlim(0, 1)
    ax_hist.set_yticks([])

    # Display cumulative distribution
    img_cdf, bins = exposure.cumulative_distribution(image, bins)
    ax_cdf.plot(bins, img_cdf, 'r')
    ax_cdf.set_yticks([])

    return ax_img, ax_hist, ax_cdf


def histogram_eq():
    # Load an example image
    img = data.moon()
    # img = io.imread('images/ISIC_0000030.jpg')

    # Equalization
    img_eq = exposure.equalize_hist(img)

    # Display results
    fig = plt.figure(figsize=(8, 5))
    axes = np.zeros((2, 2), dtype=np.object)
    axes[0, 0] = fig.add_subplot(2, 2, 1)
    for i in range(1, 2):
        axes[0, i] = fig.add_subplot(2, 2, 1+i, sharex=axes[0,0], sharey=axes[0,0])
    for i in range(0, 2):
        axes[1, i] = fig.add_subplot(2, 2, 3+i)

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img, axes[:, 0])
    ax_img.set_title('Low contrast image')

    y_min, y_max = ax_hist.get_ylim()
    ax_hist.set_ylabel('Number of pixels')
    ax_hist.set_yticks(np.linspace(0, y_max, 5))

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_eq, axes[:, 1])
    ax_img.set_title('Histogram equalization')

    # prevent overlap of y-axis labels
    fig.tight_layout()
    plt.show()


def contrast_stretching():
    # Load an example image
    img = data.moon()
    # img = io.imread('images/ISIC_0000030.jpg')

    # Contrast stretching
    p2, p98 = np.percentile(img, (2, 98))
    img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))

    # Display results
    fig = plt.figure(figsize=(8, 5))
    axes = np.zeros((2, 2), dtype=np.object)
    axes[0, 0] = fig.add_subplot(2, 2, 1)
    for i in range(1, 2):
        axes[0, i] = fig.add_subplot(2, 2, 1+i, sharex=axes[0,0], sharey=axes[0,0])
    for i in range(0, 2):
        axes[1, i] = fig.add_subplot(2, 2, 3+i)

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img, axes[:, 0])
    ax_img.set_title('Low contrast image')

    y_min, y_max = ax_hist.get_ylim()
    ax_hist.set_ylabel('Number of pixels')
    ax_hist.set_yticks(np.linspace(0, y_max, 5))

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_rescale, axes[:, 1])
    ax_img.set_title('Contrast stretching')

    # prevent overlap of y-axis labels
    fig.tight_layout()
    plt.show()


def log_compression():
    pass


def reverse_video():
    pass


def other():
    pass
