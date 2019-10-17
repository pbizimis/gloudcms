import pytest
from cmsapp.__init__ import create_app
from cmsapp.firebase_handler import process_token, FirebaseTokenVerifier, firebase_app_init
import firebase_admin
from flask import json
import firebase_admin

JWT_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImZhMWQ3NzBlZWY5ZWFhNjU0MzY1ZGE5MDhjNDIzY2NkNzY4ODkxMDUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiUGhpbGlwIEJpemltaXMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDQuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy0tX2xZd2htc25Kay9BQUFBQUFBQUFBSS9BQUFBQUFBQUFBQS9BQ0hpM3Jmek1PSU1VTHJoZWE4UXRnRDBybEZhUVhleXBBL3Bob3RvLmpwZyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9jbG91ZC1jbXMtcCIsImF1ZCI6ImNsb3VkLWNtcy1wIiwiYXV0aF90aW1lIjoxNTcxMzQ3MzE4LCJ1c2VyX2lkIjoiMlNIZjkybFZWUlhkbXo3bmJxTW5RbkduaWU4MiIsInN1YiI6IjJTSGY5MmxWVlJYZG16N25icU1uUW5HbmllODIiLCJpYXQiOjE1NzEzNDczMTksImV4cCI6MTU3MTM1MDkxOSwiZW1haWwiOiJiaXppbWlzcGhpbGlwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTE0Nzc4MjAwODkxMzM0NDE5NTkxIl0sImVtYWlsIjpbImJpemltaXNwaGlsaXBAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.yCcsmF7fI-WMBZ-l0BBwBFeGrANwBjuSLZS5Ncq01jzAof6R1zg5ZRMV1g0uz6AeGS0Ze7ubyn1aaeI8Yv07RJLMAMuIG48ZjivtHdE8zjUaGjfsShoCbzTXncMLbKqhAqmc0BU5u_8qGKm4b0w5dKd_-5ECmV3BFGQ8vNuRAmQLETjZeH5L3fU2e8uatidyqMK36DjuJ0doqytlK51g83Mmp9s2-i-g6LMjE09g-nKciry5gHXFncEIN0BtJAie7uD0TdFMcml8fZsUEnGJ0eKHMHqEoC7gbCSICnf0tzm68mIorduYxxiyLaJEJunVBjXMjfTArYyxJbkQvL8zyg"

class MockTokenVerifier():
    def verify(token):
        return {'name': 'Philip Bizimis', 'picture': 'https://lh4.googleusercontent.com/--_lYwhmsnJk/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rfzMOIMULrhea8QtgD0rlFaQXeypA/photo.jpg', 'iss': 'https://securetoken.google.com/cloud-cms-p', 'aud': 'cloud-cms-p', 'auth_time': 1571347318, 'user_id': '2SHf92lVVRXdmz7nbqMnQnGnie82', 'sub': '2SHf92lVVRXdmz7nbqMnQnGnie82', 'iat': 1571348185, 'exp': 1571351785, 'email': 'bizimisphilip@gmail.com', 'email_verified': True, 'firebase': {'identities': {'google.com': ['114778200891334419591'], 'email': ['bizimisphilip@gmail.com']}, 'sign_in_provider': 'google.com'}, 'uid': '2SHf92lVVRXdmz7nbqMnQnGnie82'}

class MockRequests():
    def get_json():
        return JWT_TOKEN

@pytest.fixture
def app():
    app = create_app({"TESTING": True,})
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        pass
    yield client


def test_post_route_success(client):
    firebase_app_init()
    #client = app.test_client()

    response = client.post("/login", json = JWT_TOKEN)

    assert response.status_code == 200
    assert response.get_data() == b"bizimisphilip@gmail.com"
   

def test_process_token():
    assert process_token(MockRequests.get_json, MockTokenVerifier.verify) == "bizimisphilip@gmail.com"


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing