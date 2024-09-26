from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, DashboardView, DashboardView, EditProfileView, CreateSiteView, EditSiteView, \
    DeleteSiteView, ProxyView

urlpatterns = [
    path("accounts/profile/", DashboardView.as_view(), name="dashboard"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('site/create/', CreateSiteView.as_view(), name='create_site'),
    path('site/edit/<int:pk>/', EditSiteView.as_view(), name='edit_site'),
    path('site/delete/<int:pk>/', DeleteSiteView.as_view(), name='delete_site'),
    path('proxy/<str:site_name>/', ProxyView.as_view(), name='proxy_site'),
    path('proxy/<str:site_name>/<path:path>/', ProxyView.as_view(), name='proxy'),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
