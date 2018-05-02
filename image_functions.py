import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # nopep8
import numpy  # nopep8
import base64  # nopep8
from skimage import exposure, filters, feature, color  # nopep8
from skimage import io as skiIO  # nopep8
import io  # nopep8
import PIL  # nopep8
from PIL import Image, ImageStat  # nopep8


def histogram_eq(img):
    """
    Takes in an image and performs histogram equalization

    :param img: Is a uint8 array
    :returns: a uint8 array of equalized image
    """
    img_eq = exposure.equalize_hist(img.astype('uint8'))
    img_eq = 255*img_eq
    return img_eq.astype('uint8')


def contrast_stretch(img):
    """
    Takes in an image and performs contrast contrast_stretching

    :param img: Is a uint8 array
    :returns: a uint8 array of contrast stretched image
    """
    p2, p98 = numpy.percentile(img, (2, 98))
    img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))
    return img_rescale.astype('uint8')


def log_compression(img):
    """
    Takes in an image and perform log compression.

    :param img: Is a uint8 array image
    :returns: a unit8 array of log compressed image
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
    :returns: a uint8 array of image with pixels inverted.
    """
    image_reverse = numpy.copy(img.astype('uint8'))
    for x in numpy.nditer(image_reverse, op_flags=['readwrite']):
        x[...] = 255 - x
    return image_reverse.astype('uint8')


def edge_detection(img):
    """
    Detects the edges of a 2D array grayscale image using
    the sobel filter and returns an image containing the edges.

    :param img: Image, 2D grayscale array, on which edge detection
    will be performed
    :returns: a uint8 array that contians the edges found through sobel
    filtering
    """
    edges = feature.canny(color.rgb2grey(img))
    edges = edges*255
    return edges.astype('uint8')


def decodeImage(image_string):
    """
    Takes in a base64 string and reconstructed into an image

    :param image_string: Base64 string representation of picture
    :returns: a reconstructed image as PIL Image object
    """
    fh = open("temp.png", "wb")
    fh.write(base64.b64decode(image_string))
    fh.close()
    img = base64.b64decode(image_string)
    img_read = skiIO.imread("temp.png")
    return img_read


def encodeImage(data_array):
    """
    Takes in a data-type returned from the data processing method to a base64
    image to be returned to the front-end

    :param data_array: array representation of image
    :return encoded_image_string: An encoded base64 string
    """
    pil_img = Image.fromarray(data_array)
    buff = io.BytesIO()
    pil_img.save(buff, format="PNG")
    encoded_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    return encoded_image_string


def imageSize(image_string):
    """
    Takes in base64 encoded and obtains the width and height

    :param image_string: base64 string representation of picture
    :returns: a list of width and height
    """

    imgdata = base64.b64decode(image_string)
    im = Image.open(io.BytesIO(imgdata))
    width, height = im.size
    dimensions = str(width) + "x" + str(height)
    return dimensions


def grayScaleDetection(image_string):
    """
    Takes in a base64 string and determines whether or not
    the image is grayscale

    :param image_string: base64 representation of the string
    :returns: a boolean of whether or not the image is grayscale
    """

    fh = open("temp2.png", "wb")
    fh.write(base64.b64decode(image_string))
    fh.close()
    im = Image.open("temp2.png").convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True
    # obtained from https://stackoverflow.com/questions/23660929/how-to-
    # check-whether-a-jpeg-image-is-color-or-gray-scale-using-only-python-stdli


def grayScaleConversion(image_string):
    """
    Takes in a base64 string, saves to a temp file, converts to
    grayscale, saves it again and returns reconstructed image as a PIL image
    object

    :param image_string: base64 string representation of picture
    :returns: a reconstructed image as PIL Image object
    """

    fh = open("tempGrayscale.png", "wb")
    fh.write(base64.b64decode(image_string))
    fh.close()
    im = Image.open("tempGrayscale.png").convert('LA')
    im.save('grayscale.png')
    img_read = skiIO.imread("grayscale.png")
    return img_read


def calculate_histogram(img, bins=256):
    """
    Takes in an image and plots(but does not display) the histogram,
    saving a base64 representation of it

    :param img: Image the histogram is being created for
    :param bins: Number of bins histogram is being divided into
    :returns: a base64 representation of histogram image
    """

    img = img.astype('uint8')
    plt.hist(img.ravel(), bins=bins, histtype='step', color='black')
    plt.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    plt.xlabel('Pixel intensity')
    plt.ylabel('Frequency')

    plt.savefig('hist.png')
    plt.clf()
    plt.cla()
    plt.close()
    # plt.show()

    hist = encodeImage(skiIO.imread('hist.png'))

    return hist
