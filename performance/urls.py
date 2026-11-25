from django.urls import path

from . import views


app_name = 'performance'

urlpatterns = [
    path(
        'metrics/<int:metric_id>/',
        views.metric_detail,
        name='metric_detail'
    ),
    path(
        'metrics/<int:metric_id>/edit/',
        views.metric_update,
        name='metric_update'
    ),
    path(
        'metrics/<int:metric_id>/delete/',
        views.metric_delete,
        name='metric_delete'
    ),
    path(
        'metrics/<int:metric_id>/entries/create/',
        views.data_entry_create,
        name='data_entry_create'
    ),
    path(
        'entries/<int:entry_id>/edit/',
        views.data_entry_update,
        name='data_entry_update'
    ),
    path(
        'entries/<int:entry_id>/delete/',
        views.data_entry_delete,
        name='data_entry_delete'
    ),
    path(
        'projects/<int:project_id>/metrics/create/',
        views.metric_create,
        name='metric_create'
    ),
]