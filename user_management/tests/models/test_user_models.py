# import pytest
# from django.core.exceptions import ValidationError
# from user_management.models import Users

# @pytest.mark.django_db
# class TestUsersModel:
#     def test_create_user(self):
#         user = Users.objects.create_user(
#             email='testuser@example.com',
#             password='TestPassword123!',
#             first_name='Test',
#             last_name='User',
#             gender='male',
#             date_of_birth='1990-01-01'
#         )
#         assert user.email == 'testuser@example.com'
#         assert user.check_password('TestPassword123!')
#         assert user.is_verified is False
#         assert user.is_superuser is False

#     def test_create_superuser(self):
#         superuser = Users.objects.create_superuser(
#             email='superuser@example.com',
#             password='SuperPassword123!'
#         )
#         assert superuser.email == 'superuser@example.com'
#         assert superuser.check_password('SuperPassword123!')
#         assert superuser.is_superuser is True

#     def test_email_uniqueness(self):
#         Users.objects.create_user(
#             email='unique@example.com',
#             password='TestPassword123!',
#             first_name='Test',
#             last_name='User',
#             gender='male',
#             date_of_birth='1990-01-01'
#         )
#         with pytest.raises(ValidationError):
#             user = Users(
#                 email='unique@example.com',
#                 password='AnotherPassword123!',
#                 first_name='Another',
#                 last_name='User',
#                 gender='female',
#                 date_of_birth='1991-01-01'
#             )
#             user.full_clean()

#     def test_required_fields(self):
#         with pytest.raises(ValidationError):
#             user = Users(
#                 email='',
#                 password='',
#                 first_name='',
#                 last_name='',
#                 gender='',
#                 date_of_birth=None
#             )
#             user.full_clean()
