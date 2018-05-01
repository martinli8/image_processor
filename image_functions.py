import numpy
import base64
from skimage import exposure, filters, feature, color
from skimage import io as skiIO
import io
import PIL
from PIL import Image, ImageStat


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
    edges = feature.canny(color.rgb2grey(img))
    edges = edges*255
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
    pil_img = Image.fromarray(data_array)
    buff = io.BytesIO()
    pil_img.save(buff, format="PNG")
    encoded_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
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
    dimensions = [width, height]
    return dimensions


def grayscaleDetection(img_path):
    """
    Function takes in a file path/image from disk and determines whether or not
    the image is grayscale
    :param img_path: Path of the image from disk
    :return boolean: Whether or not the image is grayscale (True, False)
    """

    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True
    # obtained from https://stackoverflow.com/questions/23660929/how-to-
    # check-whether-a-jpeg-image-is-color-or-gray-scale-using-only-python-stdli


def grayScaleDetection2(image_string):
    """
    Function takes in a base64 string and determines whether or not
    the image is grayscale
    :param image_string: base 64 representation of the string
    :return boolean: Whether or not the image is grayscale (True, False)
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


def grayScaleConversion(image_string):
    """
    Function takes in a base 64 string, saves to a temp file, converts to
    grayscale, saves it again and returns reconstructed image as a PIL image
    object
    :param image_string: 64bit- string representation of picture
    :return img_read: reconstructed image as PIL Image object
    """

    fh = open("tempGrayscale.png", "wb")
    fh.write(base64.b64decode(image_string))
    fh.close()
    im = Image.open("tempGrayscale.png").convert('LA')
    im.save('grayscale.png')
    img_read = skiIO.imread("grayscale.png")
    return img_read


def calculate_histogram():
    pass
