import pytest
from django.core.exceptions import ValidationError
from user_management.models import Users, UserActivities

@pytest.fixture
def create_user():
    return Users.objects.create_user(
        email='testactivityuser@example.com',
        password='TestPassword123!',
        first_name='Test',
        last_name='User',
        gender='male',
        date_of_birth='1990-01-01'
    )

@pytest.mark.django_db
class TestUserActivitiesModel:
    def test_create_activity(self, create_user):
        activity = UserActivities.objects.create(
            user_id=create_user.id,
            ip_address='192.168.0.1',
            activity_type='login'
        )
        assert activity.user_id == create_user.id
        assert activity.ip_address == '192.168.0.1'
        assert activity.activity_type == 'login'
    
    def test_invalid_ip_address(self):
        with pytest.raises(ValidationError):
            activity = UserActivities(
                ip_address='invalid_ip',
                activity_type='login'
            )
            activity.full_clean()
