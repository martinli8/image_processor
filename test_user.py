from main import *
import pytest

testUser = "testUserEmail@email.com"
picture = "12kj"
process_requested = "histogram equalization"
process_duration = 13.398
timestamp = datetime.datetime(2018, 3, 22, 13, 39, 4, 847000)
imageSize = [255, 255]


def test_create_user():
    create_user(testUser, picture, process_requested, timestamp, imageSize)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()

    assert user.email == testUser
    assert user.picture == [picture]
    assert user.process_requested == ["histogram equalization"]

    # assert user.process_duration == [13.398]
    assert user.upload_time == [datetime.datetime(2018, 3, 22, 13, 39,
                                                  4, 847000)]
    assert user.image_size == [[255, 255]]


def test_write_duration_time():
    create_user(testUser, picture, process_requested, timestamp, imageSize)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    assert write_duration_time(testUser, 6) == [6]


def test_add_user_data():
    create_user(testUser, picture, process_requested, timestamp, imageSize)
    picture_append = "zyzz"
    process_requested_append = "reverse_video"
    timestamp_append = datetime.datetime(2018, 4, 20, 4, 20, 4, 847000)
    imageSize_append = [512, 512]
    add_user_data(testUser, picture_append, process_requested_append,
                  timestamp_append, imageSize_append)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    assert user.email == testUser
    assert user.picture == [picture, picture_append]
    assert user.process_requested == ["histogram equalization",
                                      "reverse_video"]
    assert user.upload_time == [timestamp, timestamp_append]
    assert user.image_size == [[255, 255], [512, 512]]


def test_return_metadata():
    create_user(testUser, picture, process_requested, timestamp, imageSize)
    assertDict = {
        "user_email": testUser,
        "pictures": [picture],
        "process_requested": [process_requested],
        "upload_time": [timestamp],
        "image_size": [imageSize],
        "process_duration": []
    }
    assert return_metadata(testUser) == assertDict
