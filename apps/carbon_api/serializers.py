# apps/carbon_api/serializers.py
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import ContactForm
import re

class ContactFormSerializer(serializers.ModelSerializer):
    """Serializer for contact form submissions"""
    
    VALID_INTERESTS = [
        'Offset Emissions', 
        'Explore Partnership', 
        'Support Farmers', 
        'Join as a Volunteer', 
        'Other'
    ]
    
    class Meta:
        model = ContactForm
        fields = [
            'id', 'full_name', 'email', 'interests', 
            'inquiry_message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_full_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Full name must be at least 2 characters long.")
        
        # Check for valid name format (letters, spaces, hyphens, apostrophes only)
        if not re.match(r"^[a-zA-Z\s\-']+$", value.strip()):
            raise serializers.ValidationError("Full name contains invalid characters.")
        
        return value.strip()
    
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        
        # Additional email format validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Email format is invalid.")
        
        return value.lower()
    
    def validate_interests(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Interests must be a list.")
        
        if not value:
            raise serializers.ValidationError("At least one interest must be selected.")
        
        if len(value) > 5:
            raise serializers.ValidationError("Maximum 5 interests can be selected.")
        
        for interest in value:
            if interest not in self.VALID_INTERESTS:
                raise serializers.ValidationError(f"'{interest}' is not a valid interest option.")
        
        return value
    
    def validate_inquiry_message(self, value):
        if value and len(value.strip()) > 2000:
            raise serializers.ValidationError("Inquiry message cannot exceed 2000 characters.")
        
        return value.strip() if value else ""