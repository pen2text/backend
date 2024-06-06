import pytest
from datetime import date
from unittest.mock import patch
from django.db.utils import IntegrityError
from remote_handler.models import RemoteAPITokenManagers, Users  # Assuming Users model import

@pytest.mark.django_db
class TestRemoteAPITokenManagers:

    def test_remote_api_token_managers_creation(self, users):
        user_instance = users[0]

        # Mocking the uuid.uuid4 method to return a fixed UUID for testing
        with patch('uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = 'f45799c4-8f02-4d29-8e2b-7f3c2dc4831e'

            # Creating a RemoteAPITokenManagers instance
            token_manager = RemoteAPITokenManagers.objects.create(
                user=user_instance,
                name='Test Token Manager',
                token='test_token'
            )

        # Retrieving the created instance from the database to verify its correctness
        created_instance = RemoteAPITokenManagers.objects.get(id=token_manager.id)  # Use token_manager.id instead of hard-coded UUID

        # Assertions to verify the correctness of the created instance
        assert created_instance.user == user_instance
        assert created_instance.name == 'Test Token Manager'
        assert created_instance.token == 'test_token'

    def test_remote_api_token_managers_creation_without_user(self):
        with pytest.raises(IntegrityError):
            RemoteAPITokenManagers.objects.create(
                name='Test Token Manager',
                token='test_token'
            )

    def test_remote_api_token_managers_creation_with_long_name(self):
        with pytest.raises(IntegrityError):
            RemoteAPITokenManagers.objects.create(
                user=Users.objects.create(),  # Creating a dummy user object for testing
                name='a' * 256,  # Name longer than the allowed length
                token='test_token'
            )

    def test_remote_api_token_managers_creation_with_long_token(self):
        with pytest.raises(IntegrityError):
            RemoteAPITokenManagers.objects.create(
                user=Users.objects.create(),  # Creating a dummy user object for testing
                name='Test Token Manager',
                token='a' * 256,  # Token longer than the allowed length
            )
