from django.http import request
from django.shortcuts import redirect, render
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from .forms import ContactForm


class HomeView(View):
    form_class = ContactForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'index.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.send_email()
            return redirect(self.success_url)
        return render(request, 'index.html', {'form': form})

