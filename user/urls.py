from django.urls import path

from user.views import CreateUserView, CreateTokenView

urlpatterns = [
    path("login/", CreateTokenView.as_view(), name="token"),
    path("register/", CreateUserView.as_view(), name="create"),
]

app_name = "user"
