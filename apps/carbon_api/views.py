# apps/carbon_api/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
import logging

from .models import ContactForm
from .serializers import ContactFormSerializer

logger = logging.getLogger(__name__)

class ContactFormListView(generics.ListAPIView):
    """
    GET /api/contacts/
    Retrieve all contact form submissions
    """
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Optional filtering by email or name
        email = self.request.query_params.get('email')
        name = self.request.query_params.get('name')
        
        if email:
            queryset = queryset.filter(email__icontains=email)
        
        if name:
            queryset = queryset.filter(full_name__icontains=name)
        
        return queryset

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_contact_form(request):
    """
    POST /api/submit-contact/
    Submit a contact form (Transform carbon button)
    
    Expected payload:
    {
        "full_name": "John Doe",
        "email": "john@example.com",
        "interests": ["Offset Emissions", "Explore Partnership"],
        "inquiry_message": "I'm interested in carbon offset programs..."
    }
    """
    try:
        serializer = ContactFormSerializer(data=request.data)
        
        if serializer.is_valid():
            contact_form = serializer.save()
            
            # Send notification email (optional)
            try:
                send_notification_email(contact_form)
            except Exception as e:
                logger.error(f"Failed to send notification email: {str(e)}")
                # Don't fail the API call if email fails
            
            return Response({
                'success': True,
                'message': 'Your inquiry has been submitted successfully. We will get back to you soon!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Please correct the errors below.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Error in submit_contact_form: {str(e)}")
        return Response({
            'success': False,
            'message': 'An unexpected error occurred. Please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Helper function
def send_notification_email(contact_form):
    """Send notification email when new contact form is submitted"""
    if hasattr(settings, 'ADMIN_EMAIL') and settings.ADMIN_EMAIL:
        subject = f"New Contact Form Submission from {contact_form.full_name}"
        message = f"""
        New contact form submission received:
        
        Name: {contact_form.full_name}
        Email: {contact_form.email}
        Interests: {', '.join(contact_form.interests)}
        
        Message:
        {contact_form.inquiry_message}
        
        Submitted at: {contact_form.created_at}
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False
        )