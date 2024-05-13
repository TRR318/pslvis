from django.urls import path
from . import views

urlpatterns = [
    path('ex/<experiment>', views.create_subject, name='Create subject'),
    path('ex/<experiment>/<subject>/', views.index, name='index'),
    path('ex/<experiment>/<subject>/update-table', views.update_table, name='update-_table'),
    path('ex/<experiment>/<subject>/reset', views.reset, name='reset'),
    path('ex/<experiment>/<subject>/add', views.add, name='add'),
    path('ex/<experiment>/<subject>/fill', views.fill, name='fill'),
]
