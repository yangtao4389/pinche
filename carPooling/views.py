from django.shortcuts import render,HttpResponse

# Create your views here.
def Home(request):
    with open("static/carPooling/src/Home.html",'rb') as f:
        html = f.read()
    return HttpResponse(html)

