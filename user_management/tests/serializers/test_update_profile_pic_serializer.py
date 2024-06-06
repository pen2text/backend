import pytest
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from user_management.serializers import UserProfilePictureUpdateSerializer

@pytest.fixture
def mock_request():
    factory = APIRequestFactory()
    request = factory.post('/fake-url/')
    return Request(request)

def create_test_image(name="test_image.jpg", size=(100, 100), color=(255, 0, 0)):
    file = BytesIO()
    image = Image.new("RGB", size, color)
    image.save(file, 'jpeg')
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type='image/jpeg')

@pytest.mark.django_db
class TestUserProfilePictureUpdateSerializer:

    def test_validate_profile_picture_valid(self, mock_request):
        image_file = create_test_image()
        data = {'profile_picture': image_file}
        serializer = UserProfilePictureUpdateSerializer(data=data, context={'request': mock_request})
        assert serializer.is_valid()

    # def test_validate_profile_picture_invalid(self, mock_request):
    #     large_image_file = create_test_image(size=(3000, 3000))  # Creating a larger image to exceed 2 MB
    #     data = {'profile_picture': large_image_file}
    #     serializer = UserProfilePictureUpdateSerializer(data=data, context={'request': mock_request})
    #     assert not serializer.is_valid()
    #     assert 'profile_picture' in serializer.errors
    #     assert serializer.errors['profile_picture'][0] == "Profile picture size must be less than 2 MB."
