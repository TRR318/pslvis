from django.urls import path, include

from . import views
from .views import ModelHandler

urlpatterns = [

    # TODO create new experiment from get request
    # path('ex', views.create_subject, name='Create subject'),
    path('ex/', include([
        path('<ex_id>', views.create_subject, name='Create subject'),

        path('<subj_id>/', views.index, name='index'),
        path('<subj_id>/get', views.get, name='get-model'),
        path('<subj_id>/update-table', views.update_table, name='update-table'),
        path('<subj_id>/reset', views.reset, name='reset'),
        path('<subj_id>/add', views.add, name='add'),
        path('<subj_id>/fill', views.fill, name='fill'),

        path('<subj_id>/save', views.save_model, name='save'),
        path('<subj_id>/model/<model_id>', ModelHandler.as_view(), name='model')
    ]))
]
