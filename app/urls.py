from django.urls import path
from . import views

urlpatterns = [
    # TODO create new experiment from get request
    #path('ex', views.create_subject, name='Create subject'),
    path('ex/<ex_id>', views.create_subject, name='Create subject'),

    path('ex/<subj_id>/', views.index, name='index'),
    # TODO this function will be called when a button in the history is clicked. it will produce a result like update-table with no changes
    path('ex/<subj_id>/get', views.get, name='get-model'),
    path('ex/<subj_id>/update-table', views.update_table, name='update-table'),
    path('ex/<subj_id>/reset', views.reset, name='reset'),
    path('ex/<subj_id>/add', views.add, name='add'),
    path('ex/<subj_id>/fill', views.fill, name='fill'),
    
    path('ex/<subj_id>/save', views.save_model, name='save'),

    # TODO allow deleting models by a delete request. it will actually only be marked as "deleted" and not removed from db
    # https://htmx.org/attributes/hx-delete/
]
