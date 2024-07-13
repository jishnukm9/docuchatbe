from django.shortcuts import render

# Create your views here.




def home(request):

    context={}

    return render(request,"chatapp/home.html",context)



def app(request,app):

    context={}

    if app == "image":
        template = 'chatapp/imagechat.html'
    elif app == 'chat':
        template = 'chatapp/chat.html'
    else:
         template = 'chatapp/home.html'

    return render(request,template,context)


def chat(request):


    return render