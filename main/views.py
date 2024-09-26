from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponse
import requests
from django.views import View
from django.views.generic import ListView, UpdateView, DetailView, TemplateView, DeleteView
from .models import Site
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import UserRegistrationForm


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['sites'] = Site.objects.filter(user=user)
        return context


class EditProfileView(UpdateView):
    model = User
    template_name = 'edit_profile.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user


class EditSiteView(UpdateView):
    model = Site
    template_name = 'edit_site.html'
    fields = ['name', 'url']
    success_url = reverse_lazy('dashboard')


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect(self.success_url)


class DeleteSiteView(DeleteView):
    model = Site
    template_name = 'delete_site.html'
    success_url = reverse_lazy('dashboard')


class CreateSiteView(CreateView):
    model = Site
    template_name = 'create_site.html'
    fields = ['name', 'url']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProxyView(LoginRequiredMixin, View):
    def get(self, request, site_name, *args, **kwargs):
        return self.handle_request(request, site_name, *args, **kwargs)

    def post(self, request, site_name, *args, **kwargs):
        return self.handle_request(request, site_name, *args, **kwargs, method="POST")

    def handle_request(self, request, site_name, method="GET", *args, **kwargs, ):
        try:
            site = Site.objects.get(name=site_name)
        except Site.DoesNotExist:
            return HttpResponse("Site not found", status=404)

        site_url = site.url.rstrip('/')
        if kwargs.get("path"):
            path = kwargs.get("path")
            full_site_url = f"{site_url}/{path.lstrip('/')}"
        else:
            full_site_url = site.url

        sent_bytes = 0
        if method == "POST":
            sent_bytes = len(request.body)
            response = requests.post(full_site_url, data=request.POST)
        else:
            response = requests.get(full_site_url)

        soup = BeautifulSoup(response.content, 'lxml')

        base_url = urlparse(site.url).netloc
        received_bytes = len(response.content)
        site.transitions_count += 1
        site.data_sent += sent_bytes / (1024) ** 2
        site.data_received += received_bytes / (1024) ** 2
        site.save()

        for link in soup.find_all('a', href=True):
            original_url = link.get('href')
            parsed_url = urlparse(original_url)

            if parsed_url.netloc == base_url or parsed_url.netloc == '':
                proxy_url = request.build_absolute_uri(f"/proxy/{site.name}/{parsed_url.path.lstrip('/')}")
                link['href'] = proxy_url

        return HttpResponse(str(soup).encode("UTF-8"), status=response.status_code,
                            content_type=response.headers['Content-Type'])
