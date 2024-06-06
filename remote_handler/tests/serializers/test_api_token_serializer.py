import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from remote_handler.serializers import RemoteAPITokenManagerSerializer

@pytest.mark.django_db
class TestRemoteAPITokenManagerSerializer:
    factory = APIRequestFactory()
    request = factory.get('/fake-url/')
    serializer_context = {'request': Request(request)}
    
    def test_serialize_valid_data(self, remote_api_tokens):
        manager = remote_api_tokens[0]
        serializer = RemoteAPITokenManagerSerializer(instance=manager, context=self.serializer_context)
        data = serializer.data
        
        assert str(data['id']) == str(manager.id)
        assert str(data['user']) == str(manager.user.id)
        assert data['name'] == manager.name
        assert 'token' in data
        assert 'created_at' in data

    def test_serialize_read_only_fields(self, remote_api_tokens):
        manager = remote_api_tokens[0]
        serializer = RemoteAPITokenManagerSerializer(instance=manager, context=self.serializer_context)
        data = serializer.data
        
        assert 'id' in data
        assert 'user' in data
        assert 'name' in data
        assert 'token' in data
        assert 'created_at' in data

    def test_serialize_invalid_data(self):
        invalid_data = {'name': ''}
        serializer = RemoteAPITokenManagerSerializer(data=invalid_data, context=self.serializer_context)
        assert not serializer.is_valid()

        errors = serializer.errors
        
        assert 'name' in errors
