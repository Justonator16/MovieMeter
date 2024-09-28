from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view() ,name="register"),
    path("profile/<slug:username>", views.profile, name="profile"),
    path("profile/<slug:username>/update", views.profile_update ,name="profile_update"),
    path("profile/<slug:username>/delete", views.profile_delete, name="profile_delete"),
    path("logout/", LogoutView.as_view(), name="logout"),
]