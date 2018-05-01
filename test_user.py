from main import *
import pytest

testUser = "testUserEmail@email.com"
picture = test_image_processing.image_string
process_requested = "histogram equalization"
process_duration = 13.398
timestamp = datetime.datetime(2018, 3, 22, 13, 39, 4, 847000)
imageSize = "100x100"


def test_create_user():
    create_user(testUser, picture, process_requested, timestamp)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    assert user.email == testUser
    assert user.picture == [picture]
    assert user.process_requested == ["histogram equalization"]
    assert user.upload_time == [datetime.datetime(2018, 3, 22, 13, 39,
                                                  4, 847000)]


def test_write_duration_time():
    create_user(testUser, picture, process_requested, timestamp)
    assert write_duration_time(testUser, 6) == [6]
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    assert user.process_duration == [6]


def test_write_imageSize():
    create_user(testUser, picture, process_requested, timestamp)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    write_image_size(testUser, imageSize)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    assert user.image_size == ["100x100"]


def test_write_conversionFlag():
    create_user(testUser, picture, process_requested, timestamp)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    write_conversionFlag(testUser, True)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    assert user.conversion_flag == ["True"]


def test_add_user_data():
    create_user(testUser, picture, process_requested, timestamp)
    picture_append = "zyzz"
    process_requested_append = "reverse_video"
    timestamp_append = datetime.datetime(2018, 4, 20, 4, 20, 4, 847000)
    add_user_data(testUser, picture_append, process_requested_append,
                  timestamp_append)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    assert user.email == testUser
    assert user.picture == [picture, picture_append]
    assert user.process_requested == ["histogram equalization",
                                      "reverse_video"]
    assert user.upload_time == [timestamp, timestamp_append]
    assert user.image_size == ["100x100"]


def test_return_metadata():
    create_user(testUser, picture, process_requested, timestamp)
    assertDict = {
        "user_email": testUser,
        "pictures": [picture],
        "process_requested": [process_requested],
        "upload_time": [timestamp],
        "image_size": [],
        "process_duration": [],
        "conversion_flag": [],
        "processed_image_string": []
    }
    assert return_metadata(testUser) == assertDict


def test_save_filename_base64():
    create_user(testUser, picture, process_requested, timestamp)
    save_filename_base64(testUser, "asdf.png", "zyxw")
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    assert user.processed_image_string == ["zyxw"]
    assert user.processed_image_name == ["asdf.png"]
