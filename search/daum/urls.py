from django.urls import path
from .views import daum


app_name = "daum"

urlpatterns = [
    # http://127.0.0.1:8000/daum
    path("", daum, name="daum"),
]
