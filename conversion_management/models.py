from django.db import models 
from user_management.models import User 

class ConversionHistory(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    TextContent = models.TextField()
    ImageURL = models.URLField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)