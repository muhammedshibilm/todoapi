from django.urls import path
from .views import UserRegistrationAPIView,LoginView,TokenRefreshAPIView,TodoCreateView,TodoListView,TodoUpdateView,TodoDeleteView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/',LoginView.as_view(),name="user-login"),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token-refresh'),
    path('todos/create/', TodoCreateView.as_view(), name='todo-create'),
    path('todos/', TodoListView.as_view(), name='todo-list'),
    path('todos/edit/<int:todo_id>/', TodoUpdateView.as_view(), name='todo-update'),
    path('todos/delete/<int:todo_id>/', TodoDeleteView.as_view(), name='todo-delete'),
]
