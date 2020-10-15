import shutil


def test_upload_image_file(test_client):
    image = "tests/test.jpg"
    data = {
        'photo': (open(image, 'rb'), 'test.jpg'
                  )
    }
    response = test_client.post('/test/', data=data)
    assert response.status_code == 200
    assert response.json['path']
    shutil.rmtree('./files/images/test/')


def test_upload_audio_file(test_client):
    audio = "tests/Soundtest.mp3"
    data = {
        'audio': (open(audio, 'rb'), 'Soundtest.jpg')
    }
    response = test_client.post('/test/', data=data)
    assert response.status_code == 200
    assert response.json['path']
    shutil.rmtree('./files/audio/test/')


def test_upload_bad_type(test_client):
    image = "tests/test.jpg"
    data = {
        'app': (open(image, 'rb'), image)
    }
    response = test_client.post('/test/', data=data)
    assert response.status_code == 400


