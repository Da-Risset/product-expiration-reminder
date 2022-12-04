from django import forms
from django.conf import settings
from django.core.mail import send_mail

import logging


logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=600)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        """Send email using the self.cleaned_data dictionary"""
        logger.info("Sending email to %(email)s", self.cleaned_data)
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        # ... send email here
        message = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"
        send_mail(subject, message, settings.ADMIN_EMAIL, [email], fail_silently=True)




