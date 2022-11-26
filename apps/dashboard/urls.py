from django.urls import path
# TemplateView is a generic view that renders a template
from django.views.generic import TemplateView
from . import views

app_name = 'dashboard'


urlpatterns = [
    path("", views.DashboardView.as_view(), name="home"),
    path("barcode/", views.detect, name="barcode"),
    path("camera_feed/", views.camera_feed, name="camera_feed"),
    path("list-products/", TemplateView.as_view(template_name="pages/dashboard/products/list_products.html"), name="list-products"),
    path("edit-product/", TemplateView.as_view(template_name="pages/dashboard/products/edit_product.html"), name="edit-product"),
    path("add-product-kemasan/", TemplateView.as_view(template_name="pages/dashboard/products/add_product_kemasan.html"), name="add-product-kemasan"),
    path("add-product-non-kemasan/", TemplateView.as_view(template_name="pages/dashboard/products/add_product_non_kemasan.html"), name="add-product-non-kemasan"),
]

