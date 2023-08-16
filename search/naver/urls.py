from django.urls import path
from .views import naver


app_name = "naver"

urlpatterns = [
    # http://127.0.0.1:8000/naver
    path("", naver, name="naver"),
]
