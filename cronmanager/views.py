from django.shortcuts import render

# Create your views here.
def index(request):
    a = '123'
    return render(request,'crontab/index.html')
