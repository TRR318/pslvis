from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update-table/',  views.update_table, name='update-_table'),
]
