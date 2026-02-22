from django.urls import path

from task_manager.users import views

# * `GET` `/users/<int:pk>/update/` — страница редактирования пользователя
# * `POST` `/users/<int:pk>/update/` — обновление пользователя

# * `GET` `/users/<int:pk>/delete/` — страница удаления пользователя
# * `POST` `/users/<int:pk>/delete/` — удаление пользователя

urlpatterns = [
    path("", views.IndexView.as_view(), name="users_index"),
    path("create/", views.UserCreate.as_view(), name="user_create"),
]
