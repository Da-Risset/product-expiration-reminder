from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class BaseProduct(models.Model):
    LABELS = (
        ('S', 'Safety'),
        ('W', 'Warning'),
        ('D', 'Danger'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    label = models.CharField(max_length=1, choices=LABELS, default='S')
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField()

    # class Meta:
    #     abstract = True

    def save(self, **kwargs):
        slug_str = f"{self.name}-{self.expiry_date}"
        self.slug = slugify(slug_str)
        super().save(**kwargs)


class ProductPackaging(BaseProduct):
    CATEGORIES = (
        ('k_s', 'Keju & Susu'),
        ('s', 'Snack'),
        ('m', 'Minuman'),
        ('k', 'Kecantikan'),
        ('l', 'Lainnya'),
    )

    barcode = models.ForeignKey("Barcode", on_delete=models.CASCADE)
    category = models.CharField(max_length=3, choices=CATEGORIES)


class ProductNonPackaging(BaseProduct):
    QUALITY = (
        ('g', 'Good'),
        ('b', 'Bad'),
        ('m', 'Mixed'),
    )
    CATEGORIES = (
        ('b_s', 'Buah & Sayur'),
        ('d_p', 'Daging & Ikan'),
    )

    quality = models.CharField(max_length=1, choices=QUALITY)
    category = models.CharField(max_length=3, choices=CATEGORIES)


class Barcode(models.Model):
    barcode = models.CharField(max_length=43)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name





