from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, login_view
from .views import RegisterView

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy')
]

