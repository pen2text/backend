import pytest
from django.urls import reverse
from rest_framework import status
from PIL import Image
import io

@pytest.fixture
def profile_pic_url():
    return reverse('user-profile-picture-update')

@pytest.mark.django_db
class TestUserProfilePictureUpdateView:

    @pytest.fixture(autouse=True)
    def setup(self, profile_pic_url, api_client, mock_token, users):
        self.profile_pic_url = profile_pic_url
        self.api_client = api_client
        self.mock_token = mock_token
        self.users = users

    def test_update_profile_picture(self, mocker):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Create a simple image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        img_io.name = 'test.jpg' 


        mocker.patch('user_management.views.upload_image', return_value='http://example.com/image.jpg')
        response = self.api_client.patch(self.profile_pic_url, {'profile_picture': img_io}, format='multipart')

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data['status'] == 'OK'
        assert response_data['message'] == 'Profile picture updated successfully'
        assert response_data['data']['profile_picture_url'] == 'http://example.com/image.jpg'

    # def test_update_profile_picture_size_exceeded(self):
    #     user = self.users[0]
    #     token = self.mock_token(user)
    #     self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    #     # Create a large image
    #     img = Image.new('RGB', (50000, 50000), color='red')
    #     img_io = io.BytesIO()
    #     img.save(img_io, 'JPEG')
    #     img_io.seek(0)
    #     img_io.name = 'test.jpg'  


    #     response = self.api_client.patch(self.profile_pic_url, {'profile_picture': img_io}, format='multipart')

    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     response_data = response.json()
    #     assert response_data['status'] == 'FAILED'
    #     assert response_data['errors']['profile_picture'] == 'Profile picture size must be less than 2 MB'

    def test_update_profile_picture_invalid_file(self):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Create an invalid image file
        img_io = io.BytesIO(b"not an image")

        response = self.api_client.patch(self.profile_pic_url, {'profile_picture': img_io}, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        print(response.json())
        response_data = response.json()
        assert response_data['status'] == 'FAILED'
        assert response_data['message'] == 'Validation failed'
        assert response_data['errors']['profile_picture'] == 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'

    def test_update_profile_picture_unauthenticated(self):
        # Create a simple image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)

        response = self.api_client.patch(self.profile_pic_url, {'profile_picture': img_io}, format='multipart')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_data = response.json()
        assert response_data['detail'] == 'Authentication credentials were not provided.'

