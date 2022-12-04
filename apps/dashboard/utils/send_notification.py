from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from dashboard.models import ProductPackaging, ProductNonPackaging
from datetime import date, timedelta
from itertools import chain

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode


class AbstractNotification:
    def __init__(self, user):
        self.user = user

    def get_all_products_by_user(self):
        products_packs = ProductPackaging.objects.filter(user=self.user)
        products_non = ProductNonPackaging.objects.filter(user=self.user)
        # products = products_packs + products_non
        return products_packs, products_non

    def get_label(self, products_packs, products_non):
        safety = products_packs.filter(label='S').union(products_non.filter(label='S'))
        warnings = products_packs.filter(label='W').union(products_non.filter(label='W'))
        danger = products_packs.filter(label='D').union(products_non.filter(label='D'))
        return safety, warnings, danger

    def get_warning_products(self):
        products_packs, products_non = self.get_all_products_by_user()
        products = products_packs.filter(label='W').union(products_non.filter(label='W'))
        return products

    def get_expiring_products(self,):
        today = date.today()
        products_packs, products_non = self.get_all_products_by_user()
        products = products_packs.filter(expiry_date__lte=today).union(products_non.filter(expiry_date__lte=today))
        return products


class MailRecipient(AbstractNotification):
    def __init__(self, user):
        super().__init__(user)
        # self.recipient = [self.user.email]

    def send_mail(self, subject, message):
        pass


class MailAttachment(MailRecipient):
    def __init__(self, user):
        super().__init__(user)
        self.products_packs, self.products_non = self.get_all_products_by_user()
        self.safety, self.warnings, self.danger = self.get_label(self.products_packs, self.products_non)
        self.expiring_products = self.get_expiring_products()
        self.warnings_products = self.get_warning_products()

    def get_attachment(self):
        return self.safety, self.warnings, self.danger, self.expiring_products, self.warnings_products

    def get_template(self, product):
        pass


class ScheduledMail(MailAttachment):
    def __init__(self, user):
        super().__init__(user)

    def get_today_mail(self):
        users = get_user_model().objects.all()
        return [self for user in users if self.get_expiring_products(*self.get_all_products_by_user())]

    # @classmethod
    # def get_today_mail(cls):
    #     users = get_user_model().objects.all()
    #     return [cls(user) for user in users if cls(user).get_expiring_products(*cls(user).get_all_products_by_user())]

    def get_template(self, product):
        template_file = "pages/authentication/email.txt"

        range_date = product.expiry_date - date.today()

        c = {
            "username": self.user.username,
            "id": product.id,
            'name_product': product.name,
            'label_product': product.get_label_display(),
            'expiry_date': product.expiry_date,
            'expired': range_date.days,
            'signature': 'TIMELOCK',
        }
        # print(c)
        email = render_to_string(template_file, c)
        return email

    def send_scheduled_mail(self, product):

        # for product in product_label:
        subject = f"Your product {product.name} is about to expire"
        message = self.get_template(product)
        recipient = [self.user.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)
        # subject = "Expiring products in your inventory"
        # message = self.get_template()
        # recipient = self.user.email
        # send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)

    # def test_send_


