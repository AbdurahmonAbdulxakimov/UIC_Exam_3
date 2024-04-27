from django.conf import settings
from django.urls import path

from products import views as prodcut_views


app_name = "api"
urlpatterns = [
    path("", prodcut_views.ResultView.as_view()),
]
