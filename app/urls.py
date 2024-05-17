from django.urls import path
from . import views

urlpatterns = [
    #path('ex', views.create_subject, name='Create subject'),
    path('ex/<ex_id>', views.create_subject, name='Create subject'),
    path('ex/<ex_id>/<subj_id>/', views.index, name='index'),
    path('ex/<ex_id>/<subj_id>/update-table', views.update_table, name='update-_table'),
    path('ex/<ex_id>/<subj_id>/reset', views.reset, name='reset'),
    path('ex/<ex_id>/<subj_id>/add', views.add, name='add'),
    path('ex/<ex_id>/<subj_id>/fill', views.fill, name='fill'),
]
