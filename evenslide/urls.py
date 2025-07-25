from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


app_name = "evenslide"
urlpatterns = [

    path("list_evenement/", views.list_evenement, name="evenement_list"),
    path('add_evenement/', views.create_evenement, name="evenement_add"),
    path('update_evenement/<str:pk>/', views.update_evenement, name="evenement_update"),

    path("list_actions/", views.list_actions, name="action_list"),
    path("add_actions/", views.create_action, name="actions_add"),
    path("update_actions/", views.update_action, name="actions_update"),
    path('delete_actions/<int:action_id>/', views.delete_action, name='action_delete'),

    path("list_type/", views.list_type, name="type_list"),
    path("add_type/", views.create_Type, name="type_add"),
    path("update_type/", views.update_type, name="type_update"),
    path('delete_type/<int:type_id>/', views.delete_type, name='type_delete'),

    
]





