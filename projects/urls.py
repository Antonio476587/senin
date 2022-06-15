from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/create/', views.ProjectCreate.as_view(), name='project-create'),
    path('project/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project-delete'),
    path('owners/', views.OwnerListView.as_view(), name='owners'),
    path('owner/<int:pk>', views.OwnerDetailView.as_view(), name='owner-detail'),
    path('owner/<int:pk>/nickname', views.edit_owner_nickname, name='edit-owner-nickname'),
    path('owner/create/', views.OwnerCreate.as_view(), name='owner-create'),
    path('owner/<int:pk>/update/', views.OwnerUpdate.as_view(), name='owner-update'),
]