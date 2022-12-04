import logging
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from .models import ProductPackaging, ProductNonPackaging
from .utils.send_notification import ScheduledMail

logger = logging.getLogger(__name__)


def send_notification(product, label='W'):
    mail = ScheduledMail(product.user)

    mail.send_scheduled_mail(product)


# @receiver(post_save, sender=ProductPackaging)
def expiry_date_checker(product):
    today = date.today()
    if product.expiry_date <= today:
        if product.label != 'D':
            product.label = 'D'
            send_notification(product)
    elif today < product.expiry_date <= today + timedelta(days=7):
        if product.label == 'S':
            product.label = 'W'
            send_notification(product)
    else:
        product.label = 'S'
    return product


def expiry_date_checker_non(product):
    today = date.today()
    if product.expiry_date <= today:
        if product.label != 'D':
            product.label = 'D'
            product.quality = 'b'
            send_notification(product)
    elif today < product.expiry_date <= today + timedelta(days=7):
        if product.label == 'S':
            product.label = 'W'
            product.quality = 'm'
            send_notification(product)
    else:
        product.label = 'S'
        product.quality = 'g'
    return product


@receiver(user_logged_in)
def expiring_products(sender, user, request, **kwargs):
    today = date.today()
    products_packs = ProductPackaging.objects.filter(user=user)
    products_non = ProductNonPackaging.objects.filter(user=user)
    # products = products_packs.union(products_non)
    for product in products_packs:
        product = expiry_date_checker(product)
        product.save()
    for product in products_non:
        product = expiry_date_checker_non(product)
        product.save()

    logger.info('Expiring products checked')



