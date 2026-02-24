from django.urls import path

from task_manager.users import views

# * `GET` `/users/<int:pk>/delete/` — страница удаления пользователя
# * `POST` `/users/<int:pk>/delete/` — удаление пользователя

app_name = 'users'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.UserCreate.as_view(), name="create"),
    path("<int:pk>/update/", views.UserUpdate.as_view(), name="update"),
]
