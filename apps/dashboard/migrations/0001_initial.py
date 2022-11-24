# Generated by Django 4.1.3 on 2022-11-22 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Barcode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("barcode", models.CharField(max_length=13)),
                ("name", models.CharField(max_length=100)),
                ("company", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="BaseProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                (
                    "label",
                    models.CharField(
                        choices=[("S", "Safety"), ("W", "Warning"), ("D", "Danger")],
                        default="S",
                        max_length=1,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("expiry_date", models.DateField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductNonPackaging",
            fields=[
                (
                    "baseproduct_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="dashboard.baseproduct",
                    ),
                ),
                (
                    "quality",
                    models.CharField(
                        choices=[("g", "Good"), ("b", "Bad"), ("m", "Mixed")],
                        max_length=1,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[("b_s", "Buah & Sayur"), ("d_p", "Daging & Ikan")],
                        max_length=3,
                    ),
                ),
            ],
            bases=("dashboard.baseproduct",),
        ),
        migrations.CreateModel(
            name="ProductPackaging",
            fields=[
                (
                    "baseproduct_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="dashboard.baseproduct",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("k_s", "Keju & Susu"),
                            ("s", "Snack"),
                            ("m", "Minuman"),
                            ("k", "Kecantikan"),
                            ("l", "Lainnya"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "barcode",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.barcode",
                    ),
                ),
            ],
            bases=("dashboard.baseproduct",),
        ),
    ]