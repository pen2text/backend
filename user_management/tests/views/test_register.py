import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, Mock


@pytest.fixture
def register_url():
    return reverse('user-register')

@pytest.mark.django_db
def test_user_registration_success(api_client, register_url, mock_user_serializer_save, mock_send_verification_email):
    data = {
        'id': '123e4567-e89b-12d3-a456-426614174000',
        'first_name': 'John',
        'last_name': 'Doe',
        'gender': 'Male',
        'date_of_birth': '2024-05-17',
        'email': 'mie.jejaw@gmail.com',
        'password': 'Mieraf1234!',
        'is_verified': False,
        'role': 'user',
        'created_at': '2024-05-17T00:00:00Z',
        'updated_at': '2024-05-17T00:00:00Z'
    }
    mock_response = Mock(**data)
    mock_user_serializer_save.return_value = mock_response
    
    user = {
        'first_name': 'John',
        'last_name': 'Doe',
        'gender': 'Male',
        'date_of_birth': '2024-05-17',
        'email': 'mie.jejaw@gmail.com',
        'password': 'Mieraf1234!'
    }

    response = api_client.post(register_url, user, format='json')

    mock_user_serializer_save.assert_called_once()
    mock_send_verification_email.assert_called_once_with(mock_response)
    
    print(response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['status'] == 'OK'
    assert response.json()['message'] == 'User registered successfully'
    assert response.json()['data']['id'] == mock_response.id
    assert 'password' not in response.json()['data']
    
    
@pytest.mark.django_db
def test_user_registration_validation_failure(api_client, register_url):
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'gender': 'Male',
        'date_of_birth': '2024-05-17',
        'email': 'example@gmail.com'
    }

    response = api_client.post(register_url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert response_data['status'] == 'FAILED'
    assert response_data['message'] == 'Validation failed'

# @pytest.mark.django_db
# def test_user_registration_user_already_logged_in(api_client, register_url):
#     # Simulate an authenticated user
#     request = api_client.post(reverse('user-login'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
#     request.user = Mock(is_authenticated=True)
    
#     user_data = {
#         'first_name': 'John',
#         'last_name': 'Doe',
#         'gender': 'Male',
#         'date_of_birth': '2024-05-17',
#         'email': 'mie.jejaw@gmail.com',
#         'password': 'Mieraf1234!'
#     }

#     # Encode the content_type properly
#     content_type = 'application/json'
#     request_content = json.dumps(user_data).encode('utf-8')

#     response = api_client.post(register_url, data=request_content, content_type=content_type)

#     assert response.status_code == 403
#     response_data = response.json()
#     assert response_data['status'] == 'FAILED'
#     assert response_data['message'] == 'Forbidden: You are already have an active session. Please logout to create a new user account.'



# @pytest.mark.django_db
# def test_user_registration_user_already_logged_in(api_client, register_url, mocker):
#     user = Mock(is_authenticated=True)
#     api_client.force_authenticate(user=user)
    
#     user_data = {
#         'first_name': 'John',
#         'last_name': 'Doe',
#         'gender': 'Male',
#         'date_of_birth': '2024-05-17',
#         'email': 'mie.jejaw@gmail.com',
#         'password': 'Mieraf1234!'
#     }

#     response = api_client.post(register_url, user_data, format='json')

#     assert response.status_code == 403
#     response_data = response.json()
#     assert response_data['status'] == 'FAILED'
#     assert response_data['message'] == 'Forbidden: You are already have an active session. Please logout to create a new user account.'
#     api_client.force_authenticate(user=None) 
