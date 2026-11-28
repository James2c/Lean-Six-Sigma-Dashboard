from django.urls import path
from . import views


urlpatterns = [
    path(
        'projects/<int:project_id>/',
        views.fmea_dashboard,
        name='fmea_dashboard'
    ),

    path(
        'projects/<int:project_id>/failure-modes/create/',
        views.failure_mode_create,
        name='failure_mode_create'
    ),

    path(
        'projects/<int:project_id>/failure-modes/<int:failure_id>/edit/',
        views.failure_mode_edit,
        name='failure_mode_edit'
    ),

    path(
        'projects/<int:project_id>/failure-modes/<int:failure_id>/',
        views.failure_mode_detail,
        name='failure_mode_detail'
    ),

    path(
        'projects/<int:project_id>/failure-modes/<int:failure_id>/actions/create/',
        views.corrective_action_create,
        name='corrective_action_create'
    ),

    path(
        'projects/<int:project_id>/failure-modes/<int:failure_id>/actions/<int:action_id>/edit/',
        views.corrective_action_edit,
        name='corrective_action_edit'
    ),

    path(
        'projects/<int:project_id>/failure-modes/<int:failure_id>/actions/<int:action_id>/delete/',
        views.corrective_action_delete,
        name='corrective_action_delete'
    ),
]