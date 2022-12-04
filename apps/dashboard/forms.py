from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.text import slugify
from django import forms

from .models import ProductPackaging, ProductNonPackaging, Barcode
from .utils.management import label_expiry_date



class ProductPackagingForm(forms.ModelForm):
    barcode_input = forms.CharField(max_length=43, required=True)

    class Meta:
        model = ProductPackaging
        fields = ['name', 'description', 'expiry_date', 'category', 'barcode_input']
        exclude = ['user', 'slug', 'date_added', 'label', 'barcode']


class ProductNonPackagingForm(forms.ModelForm):
    class Meta:
        model = ProductNonPackaging
        fields = ['name', 'description', 'category', 'quality']
        exclude = ['user', 'slug', 'date_added', 'label', 'expiry_date']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']
        exclude = ['user', 'slug', 'date_added']


class NotificationSettingForm(forms.Form):
    MEDIA_CHOICES = (
        ('email', 'Email'),
        ('wa', 'Whatsapp'),
    )

    notification = forms.BooleanField(required=False)
    media = forms.ChoiceField(choices=MEDIA_CHOICES, required=False)
    warnings = forms.BooleanField(required=False)

    def send_mail_to_admin(self, user):
        subject = f"Notif Expiring Products for {user.username}"
        message = f"Notification Settings for {user.username} has been changed\n" \
                  f"Notif me? : {self.cleaned_data['notification']}\n" \
                  f"Email: {self.cleaned_data['media']}\n" \
                  f"If warnings? : {self.cleaned_data['warnings']}"
        recipient = [settings.ADMIN_EMAIL]

        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)


