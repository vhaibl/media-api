import shutil


def test_download_image_file(test_client):
    image = "tests/test.jpg"
    data = {
        'photo': (open(image, 'rb'), 'test.jpg')
    }
    response = test_client.post('/test/', data=data)
    getimage = test_client.get(response.json['path'])

    assert getimage.headers['Content-Length'] == str(35758)
    shutil.rmtree('./files/images/test/')
    assert response.status_code == 200

def test_download_audio_file(test_client):
    audio = "tests/Soundtest.mp3"
    data = {
        'audio': (open(audio, 'rb'), 'Soundtest.mp3')
    }
    response = test_client.post('/test/', data=data)
    getimage = test_client.get(response.json['path'])

    assert getimage.headers['Content-Length'] == str(38579)
    shutil.rmtree('./files/audio/test/')
    assert response.status_code == 200


def test_not_found(test_client):
    response = test_client.get('/media/test.app')
    assert response.status_code == 404