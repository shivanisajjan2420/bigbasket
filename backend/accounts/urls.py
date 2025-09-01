from django.urls import path, include
from django.http import HttpResponse

def greeting(request):
    return HttpResponse("Hello, welcome to the accounts section!")

urlpatterns = [
   path('', greeting)
]
