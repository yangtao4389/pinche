from django.shortcuts import render,HttpResponse,HttpResponseRedirect

# Create your views here.
def Home(request):
    # return HttpResponseRedirect("/static/carPooling/src/Home.html")
    with open("static/carPooling/src/Home.html",'rb') as f:
        html = f.read()
    return HttpResponse(html)



def AssList(request):
    return HttpResponseRedirect("/static/carPooling/src/AssList.html")