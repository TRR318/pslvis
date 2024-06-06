from django.urls import path, include

from . import views
from .views import ModelHandler

urlpatterns = [

    path('ex/', include([
        # TODO create new experiment from get request
        # path('ex', views.create_subject, name='Create subject'),
        path('<ex_id>', views.create_subject, name='Create subject'),

        path('<subj_id>/', views.index, name='index'),
        # TODO this function will be called when a button in the history is clicked. it will produce a result like update-table with no changes
        path('<subj_id>/get', views.get, name='get-model'),
        path('<subj_id>/update-table', views.update_table, name='update-table'),
        path('<subj_id>/reset', views.reset, name='reset'),
        path('<subj_id>/add', views.add, name='add'),
        path('<subj_id>/fill', views.fill, name='fill'),

        #path('<subj_id>/save', views.save_model, name='save'),
        path('<subj_id>/model/<model_id>', ModelHandler.as_view(), name='model'),

        # TODO allow deleting models by a delete request. it will actually only be marked as "deleted" and not removed from db
        # https://htmx.org/attributes/hx-delete/
    ]))
]
