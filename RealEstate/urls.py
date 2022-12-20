"""RealEstate url Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a url to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a url to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a url to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Configurations import views as configuration_views
from Settings import views as setting_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', configuration_views.index, name='index'),
    path('configuration/', configuration_views.configurations),
    path('settings/', setting_views.index, name='settings'),
    path('setting/', setting_views.settings, name='setting'),
]
