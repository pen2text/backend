import pytest
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError
from chapa_gateway.models import ChapaTransactions, ChapaStatus  

@pytest.mark.django_db
class TestChapaTransactions:

    @pytest.fixture
    def chapa_transaction(self):
        return ChapaTransactions.objects.create(
            amount=100.0,
            currency='ETB',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            payment_title='Test Payment',
            description='Test Description',
            status=ChapaStatus.CREATED,
            response_dump={"key": "value"},
            checkout_url='https://example.com/checkout'
        )

    def test_chapa_transaction_creation(self, chapa_transaction):
        # Assertions to verify the correctness of the created instance
        assert chapa_transaction.amount == 100.0
        assert chapa_transaction.currency == 'ETB'
        assert chapa_transaction.email == 'test@example.com'
        assert chapa_transaction.first_name == 'Test'
        assert chapa_transaction.last_name == 'User'
        assert chapa_transaction.payment_title == 'Test Payment'
        assert chapa_transaction.description == 'Test Description'
        assert chapa_transaction.status == ChapaStatus.CREATED
        assert chapa_transaction.response_dump == {"key": "value"}
        assert chapa_transaction.checkout_url == 'https://example.com/checkout'

    def test_chapa_transaction_creation_without_email(self):
        invalid_transaction = ChapaTransactions(
            amount=100.0,
            currency='ETB',
            first_name='Test',
            last_name='User',
            payment_title='Test Payment',
            description='Test Description',
            status=ChapaStatus.CREATED
        )
        with pytest.raises(ValidationError):
            invalid_transaction.full_clean()  # This will trigger the validation

    def test_chapa_transaction_creation_with_long_email(self):
        with pytest.raises(DataError):
            ChapaTransactions.objects.create(
                amount=100.0,
                currency='ETB',
                email='a' * 255 + '@example.com',  # Email longer than the allowed length
                first_name='Test',
                last_name='User',
                payment_title='Test Payment',
                description='Test Description',
                status=ChapaStatus.CREATED
            )

    def test_chapa_transaction_creation_with_invalid_status(self):
        with pytest.raises(ValidationError):
            invalid_transaction = ChapaTransactions(
                amount=100.0,
                currency='ETB',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                payment_title='Test Payment',
                description='Test Description',
                status='invalid_status'
            )
            invalid_transaction.full_clean()  # This triggers model validation

    def test_chapa_transaction_creation_with_negative_amount(self):
        with pytest.raises(ValidationError):
            invalid_transaction = ChapaTransactions(
                amount=-100.0,  # Negative amount
                currency='ETB',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                payment_title='Test Payment',
                description='Test Description',
                status=ChapaStatus.CREATED
            )
            invalid_transaction.full_clean()  # This triggers model validation

    def test_chapa_transaction_default_values(self):
        transaction = ChapaTransactions.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
        )
        assert transaction.amount == 0.0
        assert transaction.currency == 'ETB'
        assert transaction.payment_title == 'Payment'
        assert transaction.description == 'Payment Description'
        assert transaction.status == ChapaStatus.CREATED
        assert transaction.response_dump == {}

