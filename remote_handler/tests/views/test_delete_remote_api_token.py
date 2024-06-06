import uuid
import pytest
from remote_handler.models import RemoteAPITokenManagers
from rest_framework import status
from django.urls import reverse
# from package_manager.models import RemoteAPITokenManagers


@pytest.fixture
def delete_url():
    def _delete_url(token_id):
        return reverse('remote-api-token-delete', kwargs={'id': token_id})
    return _delete_url

@pytest.mark.django_db
class TestRemoteAPITokenManagerDeleteView:
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, users, mock_token, remote_api_tokens):
        self.api_client = api_client
        self.users = users
        self.mock_token = mock_token
        self.remote_api_tokens = remote_api_tokens

    def test_remote_api_token_manager_delete_unauthorized(self, delete_url):
        token_id = self.remote_api_tokens[0].id
        response = self.api_client.delete(delete_url(token_id))
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_remote_api_token_manager_delete_not_found(self, delete_url):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        non_existing_token_id = uuid.uuid4()
        response = self.api_client.delete(delete_url(non_existing_token_id))
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Remote API Token Not Found'

    def test_remote_api_token_manager_delete_forbidden(self, delete_url):
        user = self.users[1]  # User without the token
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        token_id = self.remote_api_tokens[0].id  # Token belonging to another user
        response = self.api_client.delete(delete_url(token_id))
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Remote API Token Not Found'

    def test_remote_api_token_manager_delete_success(self, delete_url):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        token_id = self.remote_api_tokens[0].id
        response = self.api_client.delete(delete_url(token_id))
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'Remote API Token Deleted'
        
        #Ensure the token is actually deleted
        with pytest.raises(RemoteAPITokenManagers.DoesNotExist):
            RemoteAPITokenManagers.objects.get(id=token_id)
