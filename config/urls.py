from django.contrib import admin
from django.urls import path, include
from core import views
from dmaic import urls as dmaic_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('projects/', include('projects.urls')),
    path('dmaic/', include(dmaic_urls)),
]