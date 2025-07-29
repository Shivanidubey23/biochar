# apps/carbon_api/urls.py
from django.urls import path
from . import views

app_name = 'carbon_api'

urlpatterns = [
    # Contact form endpoints
    path('contacts/', views.ContactFormListView.as_view(), name='get_contacts'),  # GET - retrieve submissions
    path('submit-contact/', views.submit_contact_form, name='submit_contact'),    # POST - submit form
]