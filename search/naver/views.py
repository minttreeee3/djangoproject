from django.shortcuts import render
from django.http import HttpResponse

from .models import NaverData


# Create your views here.
def naver(request):
    naver = NaverData.objects.all()
    context = {"naver": naver}
    # 정보를 전달
    return render(request, "naver.html", context)


# 홈화면
def index(request):
    # index.html 템플릿
    return render(request, "index.html")
