from django.shortcuts import render
from django.http import HttpResponse

from .models import DaumData


# Create your views here.
def daum(request):
    daum = DaumData.objects.all()
    context = {"daum": daum}
    # 정보를 전달
    return render(request, "daum.html", context)
