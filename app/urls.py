from django.urls import path
from . import views

urlpatterns = [
    path('<experiment>', views.create_subject, name='Create subject'),
    path('<experiment>/<subject>', views.index, name='index'),
    path('<experiment>/<subject>/update-table/', views.update_table, name='update-_table'),
]
