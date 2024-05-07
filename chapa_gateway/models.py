from django.db import models
import uuid

class ChapaStatus(models.TextChoices):
    CREATED = 'created', 'CREATED'
    PENDING = 'pending', 'PENDING'
    SUCCESS = 'success', 'SUCCESS'
    FAILED = 'failed', 'FAILED'

class ChapaTransactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField(default=0.0)
    currency = models.CharField(max_length=25, default='ETB')
    email = models.EmailField()
    phone_number = models.CharField(max_length=25)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    payment_title = models.CharField(max_length=20, default='Payment')
    description = models.TextField(default='Payment Description')

    status = models.CharField(max_length=50, choices=ChapaStatus.choices, default=ChapaStatus.CREATED)
    response_dump = models.JSONField(default=dict, blank=True)  # incase the response is valuable in the future
    checkout_url = models.URLField(null=True, blank=True)
    
    class Meta:
        db_table = 'chapa_transactions'
        
