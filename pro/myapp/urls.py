"""pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.myfunc,name="myindex"),
    path("mydata/",views.data,name="mydata"),
    path("delete/<int:id>",views.delete,name="delete"),
    path("update/<int:id>",views.update,name="update"),
    # path("",views.mylogin,name='mylogin'),
    # path('main/',views.mainpage, name='mainpage'),
    # path('mylogout/',views.mylogout,name='mylogout'),
    # path('mysignup/',views.mysignup,name='mysignup'),
    # path("activate/<str:id>/",views.activate,name='activate')
]
