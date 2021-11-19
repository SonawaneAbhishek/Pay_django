from . import views
from django.urls import path,include

urlpatterns = [
    path('',views.home,name='home'),
    path('success/',views.success,name='success'),
]