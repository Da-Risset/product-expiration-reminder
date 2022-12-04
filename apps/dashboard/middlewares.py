from . import models

from django.db.models import Q

from datetime import date, timedelta

from itertools import chain


def notification_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            products_packs_warnings = models.ProductPackaging.objects.filter(user=request.user).filter(label='W')
            products_non_warnings = models.ProductNonPackaging.objects.filter(user=request.user).filter(label='W')
            products_packs_danger = models.ProductPackaging.objects.filter(user=request.user).filter(label='D')
            products_non_danger = models.ProductNonPackaging.objects.filter(user=request.user).filter(label='D')
            today = date.today()
            products_warning = products_packs_warnings.union(products_non_warnings)
            products_danger = products_packs_danger.union(products_non_danger)
            products = products_warning.union(products_danger)
            # request.products = products
            if products:
                request.notification = products
            else:
                request.notification = None
        else:
            request.notification = False
        response = get_response(request)
        return response
    return middleware