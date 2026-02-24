from django.urls import path

from task_manager.users import views

app_name = 'users'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.UserCreate.as_view(), name="create"),
    path("<int:pk>/update/", views.UserUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.UserDelete.as_view(), name="delete"),
]
