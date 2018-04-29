import numpy
import base64
from skimage import exposure, filters
from skimage import io as skiIO
import io
import PIL
from PIL import Image


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
    img_read = skiIO.imread("temp.png")
    return img_read


def encodeImage(data_array):
    """
    Function will take in a data-type returned from the data processing method
    to a base 64 image to be returned to the front-end
    :param img: Unit-8 array
    :return encoded_image_string: An encoded image String of base 64
    """
    print(type(data_array))
    encoded_image_string = base64.b64encode(data_array)
    return encoded_image_string

def imageSize(image_string):
    """
    Function takes in base64 encoded and obtains the width and Height
    :param image_string: 64bit - string represtnation of picture
    :return dimensions: List of width and height
    """
    imgdata = base64.b64decode(image_string)
    im = Image.open(io.BytesIO(imgdata))
    width, height = im.size
    dimensions = [width,height]
    return dimensions
