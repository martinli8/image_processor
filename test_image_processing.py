from main import *
import pytest
from PIL import Image
import numpy as np
from skimage import color
from skimage import io

image_string = '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'


def test_histogram_eq():
    img_rev_truth = io.imread('hist_eq.png')
    img_rev_truth = img_rev_truth.astype('uint8')
    img_original = io.imread('Small.png')
    image_hist = histogram_eq(img_original)
    assert np.array_equal(image_hist, img_rev_truth)


def test_contrast_stretching():
    img_rev_truth = io.imread('contrast_stretch.png')
    img_rev_truth = img_rev_truth.astype('uint8')
    img_original = io.imread('Small.png')
    image_stretch = contrast_stretch(img_original)
    assert np.array_equal(image_stretch, img_rev_truth)

    
def test_log_compression():
    img_rev_truth = io.imread('log_image.png')
    img_rev_truth = img_rev_truth.astype('uint8')
    img_original = io.imread('Small.png')
    image_log  = log_compression(img_original)
    assert np.array_equal(image_log, img_rev_truth)


def test_reverse_video():
    img_rev_truth = io.imread('reverse.png')
    img_rev_truth = img_rev_truth.astype('uint8')
    img_original = io.imread('Small.png')
    img_rev = reverse_video(img_original)
    assert np.array_equal(img_rev_truth, img_rev)


def test_edge_detection():
    img = color.rgb2gray(io.imread('edges.jpg'))
    img_original = color.rgb2gray(io.imread('Small.png'))
    img_edge_compute = edge_detection(img_original)
    assert np.array_equal(img, img_edge_compute)


def test_decodeImage():
    original_img = Image.open('Small.png')
    img_decode = decodeImage(image_string)
    assert original_img == img_decode

    
def test_encodeImage():
    original_img = io.imread('Small.png')
    output = encodeImage(original_img)
    assert output == output
