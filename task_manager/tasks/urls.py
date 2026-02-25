from django.urls import path

from task_manager.tasks import views

app_name = 'tasks'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"), 
    path("create/", views.TaskCreate.as_view(), name="create"), 
    path("<int:pk>/update/", views.TaskUpdate.as_view(), name="update"), 
    path("<int:pk>/delete/", views.TaskDelete.as_view(), name="delete"),
    path("<int:pk>/", views.TaskDetail.as_view(), name="detail"),
]
