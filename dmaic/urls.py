from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.dmaic_project_list,
        name='dmaic_project_list'
    ),

    path(
        'project/<int:project_id>/',
        views.dmaic_workspace,
        name='dmaic_workspace'
    ),

    path(
        'project/<int:project_id>/phase/<int:phase_id>/',
        views.dmaic_phase_detail,
        name='dmaic_phase_detail'
    ),

    path(
        'project/<int:project_id>/phase/<int:phase_id>/deliverable/create/',
        views.deliverable_create,
        name='deliverable_create'
    ),

    path(
        'project/<int:project_id>/phase/<int:phase_id>/deliverable/<int:deliverable_id>/edit/',
        views.deliverable_edit,
        name='deliverable_edit'
    ),

    path(
        'project/<int:project_id>/phase/<int:phase_id>/deliverable/<int:deliverable_id>/delete/',
        views.deliverable_delete,
        name='deliverable_delete'
    ),

]