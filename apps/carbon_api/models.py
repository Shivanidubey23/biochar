# apps/carbon_api/models.py
from django.db import models
from django.core.validators import EmailValidator
import uuid

class ContactForm(models.Model):
    """Model for contact form submissions - Transform carbon button saves this data"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    interests = models.JSONField(default=list)  # ["Offset Emissions", "Explore Partnership", etc.]
    inquiry_message = models.TextField(blank=True)  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.email}"
    
    class Meta:
        ordering = ['-created_at']