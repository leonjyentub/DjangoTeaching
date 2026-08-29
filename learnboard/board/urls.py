from django.urls import path

from . import views

app_name = "board"

urlpatterns = [
    path("", views.MessageListView.as_view(), name="list"),
    path("register/", views.register, name="register"),
    path("new/", views.MessageCreateView.as_view(), name="create"),
    path("messages/<int:pk>/edit/", views.MessageUpdateView.as_view(), name="update"),
    path("messages/<int:pk>/delete/", views.MessageDeleteView.as_view(), name="delete"),
]
