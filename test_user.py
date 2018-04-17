from main import *
import pytest

testUser = "testUserEmail@email.com"
picture = "12kj"
process_requested = "histogram equalization"
process_duration = 13.398
timestamp = datetime.datetime(2018, 3, 22, 13, 39, 4, 847000)
imageSize = [255,255]

def test_create_user():
    create_user(testUser, picture, process_requested, timestamp, imageSize)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()

    assert user.email == testUser
    assert user.picture == [picture]
    assert user.process_requested == ["histogram equalization"]
    # assert user.process_duration == [13.398]
    assert user.upload_time == [datetime.datetime(2018, 3, 22,
                                                       13, 39, 4, 847000)]
    assert user.image_size == [[255,255]]

def test_write_duration_time():
    create_user(testUser, picture, process_requested, timestamp, imageSize)
    user = models.User.objects.raw({"_id": "testUserEmail@email.com"}).first()
    assert write_duration_time(testUser, 6) == [6]
