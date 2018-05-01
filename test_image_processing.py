from main import *
import pytest
from PIL import Image
import numpy as np
from skimage import color
from skimage import io

f = open('images/image_code.txt', "r")
image_string = f.read().replace('\n', '')


def test_histogram_eq():
    img_rev_truth = io.imread('images/hist_eq.png')
    img_rev_truth = img_rev_truth.astype('uint8')
    img_original = io.imread('images/Small.png')
    image_hist = histogram_eq(img_original)
    assert np.array_equal(image_hist, img_rev_truth)


def test_contrast_stretching():
    img_rev_truth = io.imread('images/contrast_stretch.png')
    img_rev_truth = img_rev_truth.astype('uint8')
    img_original = io.imread('images/Small.png')
    image_stretch = contrast_stretch(img_original)
    assert np.array_equal(image_stretch, img_rev_truth)


def test_log_compression():
    img_rev_truth = io.imread('images/log_image.png')
    img_rev_truth = img_rev_truth.astype('uint8')
    img_original = io.imread('images/Small.png')
    image_log = log_compression(img_original)
    assert np.array_equal(image_log, img_rev_truth)


def test_reverse_video():
    img_rev_truth = io.imread('images/reverse.png')
    img_rev_truth = img_rev_truth.astype('uint8')
    img_original = io.imread('images/Small.png')
    img_rev = reverse_video(img_original)
    assert np.array_equal(img_rev_truth, img_rev)


def test_edge_detection():
    img = color.rgb2gray(io.imread('images/edges.png'))
    img_original = color.rgb2gray(io.imread('images/Small.png'))
    img_edge_compute = edge_detection(img_original)
    assert np.array_equal(img, img_edge_compute)


def test_decodeImage():
    original_img = io.imread('images/Small.png')
    img_decode = decodeImage(image_string)
    assert original_img.all() == img_decode.all()


def test_encodeImage():
    original_img = io.imread('images/Small.png')
    output = encodeImage(original_img)
    assert output == image_string


def test_process_image():
    testUser = "testUserEmail@email.com"
    process_requested = "contrast_stretching"
    process_duration = 13.398
    timestamp = datetime.datetime(2018, 3, 22, 13, 39, 4, 847000)
    imageSize = [255, 255]
    create_user(testUser, image_string, process_requested,
                timestamp)
    assert process_image(testUser, process_requested,
                         image_string) == encodeImage(
        contrast_stretch(decodeImage(image_string)))


def test_save_image():
    testUser = "testUserEmail@email.com"
    save_image(testUser, image_string, "PRE")
    original_image = io.imread('images/Small.png')
    processed_image = io.imread('testUserEmail_pre_1.png')
    assert original_image.all() == processed_image.all()


def test_image_size():
    assert imageSize(image_string) == [100, 100]


def test_grayscaleDetection():
    assert grayscaleDetection('images/Small.png') is False
    assert grayscaleDetection('images/image.png') is True


def test_grayscaleDetection2():
    assert grayScaleDetection2(image_string) is False
    output = encodeImage(io.imread('images/image.png'))
    assert grayScaleDetection2(output) is True


def test_grayscaleConversion():
    assert grayScaleConversion(image_string).all() == skiIO.imread(
                                                    "images/image.png").all()
