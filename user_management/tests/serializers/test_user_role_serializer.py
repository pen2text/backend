import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, force_authenticate
from user_management.serializers import RoleSerializer

@pytest.fixture
def mock_request():
    factory = APIRequestFactory()
    request = factory.post('/fake-url/')
    return Request(request)

@pytest.mark.django_db
class TestRoleSerializer:
    def test_validation(self, mock_request, users):
        user = users[0]
        data = {'id': user.id, 'role': 'admin'}
        serializer = RoleSerializer(data=data, context={'request': mock_request})
        
        assert serializer.is_valid()

    def test_invalid_role(self, mock_request, users):
        user = users[0]
        data = {'id': user.id, 'role': 'invalid_role'}
        serializer = RoleSerializer(data=data, context={'request': mock_request})
        
        assert not serializer.is_valid()
        assert 'role' in serializer.errors

    def test_cannot_change_own_role(self, mock_request, users):
        user = users[0]
        data = {'id': user.id, 'role': 'admin'}
        request = mock_request
        request.user = user
        force_authenticate(request, user=user)
        serializer = RoleSerializer(data=data, context={'request': request})
        
        assert not serializer.is_valid()
        assert 'id' in serializer.errors
        
    def test_update(self, mock_request, users):

        serializer = RoleSerializer(instance=users[1], data={'role': 'user'}, partial=True, context={'request': mock_request})
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.role == 'user'
