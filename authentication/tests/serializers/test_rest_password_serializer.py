import pytest
from unittest.mock import patch
from authentication.serializers import ResetPasswordSerializer
from user_management.models import Users

@pytest.mark.django_db
class TestResetPasswordSerializer:

    @patch('authentication.serializers.verify_token')
    def test_valid_data(self, mock_verify_token, users):
        mock_verify_token.return_value = users[0]
        data = {
            'token': 'valid_token',
            'password': 'ValidPass123!'
        }
        serializer = ResetPasswordSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['password'] == data['password']
        assert serializer.validated_data['token'] == data['token']
        serializer.save()
        users[0].refresh_from_db()
        assert users[0].check_password(data['password'])

    @patch('authentication.serializers.verify_token')
    def test_invalid_token(self, mock_verify_token):
        mock_verify_token.side_effect = Exception("Invalid token")
        data = {
            'token': 'invalid_token',
            'password': 'ValidPass123!'
        }
        serializer = ResetPasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert 'token' in serializer.errors

    def test_invalid_password_length(self):
        data = {
            'token': 'valid_token',
            'password': 'Short1!'
        }
        serializer = ResetPasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
        assert "Password must be at least 8 characters long." in serializer.errors['password']

    def test_invalid_password_no_uppercase(self):
        data = {
            'token': 'valid_token',
            'password': 'validpass123!'
        }
        serializer = ResetPasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
        assert "Password must contain at least one upper-case letter." in serializer.errors['password']

    def test_invalid_password_no_digit(self):
        data = {
            'token': 'valid_token',
            'password': 'Validpass!'
        }
        serializer = ResetPasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
        assert "Password must contain at least one digit." in serializer.errors['password']

    def test_invalid_password_no_special_char(self):
        data = {
            'token': 'valid_token',
            'password': 'Validpass123'
        }
        serializer = ResetPasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
        assert "Password must contain at least one special character." in serializer.errors['password']

    @patch('authentication.serializers.verify_token')
    def test_invalid_password_multiple_errors(self, mock_verify_token):
        mock_verify_token.return_value = Users(
            email='test@example.com',
            password='old_password'
        )
        data = {
            'token': 'valid_token',
            'password': 'short'
        }
        serializer = ResetPasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
        assert "Password must be at least 8 characters long." in serializer.errors['password']
        assert "Password must contain at least one upper-case letter." in serializer.errors['password']
        assert "Password must contain at least one digit." in serializer.errors['password']
        assert "Password must contain at least one special character." in serializer.errors['password']
