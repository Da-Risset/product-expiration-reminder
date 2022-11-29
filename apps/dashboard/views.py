from django.http import request, StreamingHttpResponse, JsonResponse, HttpResponse
from django.shortcuts import redirect, render, reverse
from django.utils.text import slugify
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from . import models
import os
import time
from datetime import datetime
from PIL import Image
from pyzbar.pyzbar import decode

from .utils.camera_streaming import CameraStreamingWidget
from .forms import ProductPackagingForm, ProductNonPackagingForm

from .utils.management import label_expiry_date, ExpiryDateManage


# from utils.camera_streaming import CameraStreamingWidget


class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        print(request.session)
        greeting = {}
        greeting['title'] = "Dashboard"
        greeting['pageview'] = "Timelock"
        return render(request, 'menu/index.html',greeting)


def camera_feed(request):
    stream = CameraStreamingWidget()
    frames = stream.get_frames()

    # if ajax request is sent
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        barcode_data = None
        file_saved_at = None
        barcode_name = ''
        print('Ajax request received')
        time_stamp = str(datetime.now().strftime("%d-%m-%y"))
        image = os.path.join(os.getcwd(), "media",
                             "images", f"img_{time_stamp}.png")
        if os.path.exists(image):
            # open image if exists
            im = Image.open(image)
            # decode barcode
            if decode(im):
                for barcode in decode(im):
                    barcode_data = (barcode.data).decode('utf-8')
                    file_saved_at = time.ctime(os.path.getmtime(image))
                    # return decoded barcode as json response

                if models.Barcode.objects.filter(barcode=str(barcode_data)).exists():
                    barcode_name = models.Barcode.objects.filter(barcode=str(barcode_data)).first()
                    return JsonResponse(data={'barcode_data': barcode_data, 'file_saved_at': file_saved_at, 'barcode_name': barcode_name.name})
                return JsonResponse(data={'barcode_data': barcode_data, 'file_saved_at': file_saved_at, 'barcode_name': barcode_name})
            else:
                return JsonResponse(data={'barcode_data': None})
        else:
            return JsonResponse(data={'barcode_data': None})
    # else stream the frames from camera feed
    else:
        return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')


def add_barcode(request):
    # stream = CameraStreamingWidget()
    # success, frame = stream.camera.read()
    # if success:
    #     status = True
    # else:
    #     status = False
    status = open_camera()
    return render(request, 'pages/dashboard/barcode/add_barcode.html', context={'cam_status': status})


def open_camera():
    stream = CameraStreamingWidget()
    success, frame = stream.camera.read()
    if success:
        status = True
    else:
        status = False
    return status


class BarcodeListView(LoginRequiredMixin, ListView):
    model = models.Barcode
    template_name = 'pages/dashboard/barcode/list_barcode.html'
    context_object_name = 'barcodes'
    ordering = ['name']
    paginate_by = 1000

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List Barcode'
        context['pageview'] = 'Barcode'
        return context


class BarcodeCreateView(LoginRequiredMixin, CreateView):
    model = models.Barcode
    fields = '__all__'
    template_name = 'pages/dashboard/barcode/add_barcode.html'

    def get_success_url(self):
        return reverse('dashboard:list-barcode')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = open_camera()
        context['cam_status'] = status
        context['pageview'] = "Timelock"
        context['title'] = "Add Barcode"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductPackagingListView(LoginRequiredMixin, ListView):
    model = models.ProductPackaging
    template_name = 'pages/dashboard/products/list_product_kemasan.html'
    context_object_name = 'products'
    ordering = ['name']
    paginate_by = 1000

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List Product Packaging'
        context['pageview'] = 'Product'
        return context


class ProductPackagingCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductPackagingForm

    template_name = 'pages/dashboard/products/add_product_kemasan.html'

    def get_success_url(self):
        return reverse('dashboard:list-products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageview'] = "Timelock"
        context['title'] = "Add Product Packaging"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        barcode = self.request.POST.get('barcode_input')
        if models.Barcode.objects.filter(barcode=barcode).exists():
            barcode = models.Barcode.objects.filter(barcode=barcode).first()
        else:
            return HttpResponse('Barcode not found')

        self.object.barcode = barcode
        self.object.slug = slugify(self.object.name + "-" + self.object.expiry_date.strftime("%d-%m-%y"))
        self.object.label = label_expiry_date(self.object.expiry_date)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductNonPackagingListView(LoginRequiredMixin, ListView):
    model = models.ProductNonPackaging
    template_name = 'pages/dashboard/products/list_product_non_kemasan.html'
    context_object_name = 'products'
    ordering = ['name']
    paginate_by = 1000

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List Product Non Packaging'
        context['pageview'] = 'Product'
        return context


class ProductNonPackagingCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductNonPackagingForm

    template_name = 'pages/dashboard/products/add_product_non_kemasan.html'

    def get_success_url(self):
        return reverse('dashboard:list-products-nonkemasan')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageview'] = "Timelock"
        context['title'] = "Add Product Non Packaging"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        name = self.request.POST.get('name').lower()
        quality = self.request.POST.get('quality')

        ex = ExpiryDateManage(name, quality)
        label, expiry_date = ex.get_expiry_date_label()

        self.object.slug = slugify(self.object.name + "-" + expiry_date.strftime("%d-%m-%y"))
        self.object.label = label
        self.object.expiry_date = expiry_date
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductPackagingUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ProductPackaging
    form_class = ProductPackagingForm

    template_name = 'pages/dashboard/products/add_product_kemasan.html'

    def get_success_url(self):
        return reverse('dashboard:list-products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageview'] = "Timelock"
        context['title'] = "Update Product Packaging"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        barcode = self.request.POST.get('barcode_input')
        if models.Barcode.objects.filter(barcode=barcode).exists():
            barcode = models.Barcode.objects.filter(barcode=barcode).first()
        else:
            return HttpResponse('Barcode not found')

        self.object.barcode = barcode
        self.object.slug = slugify(self.object.name + "-" + self.object.expiry_date.strftime("%d-%m-%y"))
        self.object.label = label_expiry_date(self.object.expiry_date)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

