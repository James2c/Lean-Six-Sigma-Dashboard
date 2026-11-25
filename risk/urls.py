from django.urls import path

from . import views


urlpatterns = [
    path(
        'projects/<int:project_id>/',
        views.risk_list,
        name='risk_list'
    ),
    path(
        'projects/<int:project_id>/matrix/',
        views.risk_matrix,
        name='risk_matrix'
    ),
    path(
        'projects/<int:project_id>/create/',
        views.risk_create,
        name='risk_create'
    ),
    path(
        'projects/<int:project_id>/<int:risk_id>/edit/',
        views.risk_edit,
        name='risk_edit'
    ),
    path(
        'projects/<int:project_id>/<int:risk_id>/delete/',
        views.risk_delete,
        name='risk_delete'
    ),
    path(
        'projects/<int:project_id>/<int:risk_id>/',
        views.risk_detail,
        name='risk_detail'
    ),
]