from django.urls import path

from user.views import CreateUserView, CreateTokenView, ManageUserView

urlpatterns = [
    path("login/", CreateTokenView.as_view(), name="token"),
    path("register/", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
