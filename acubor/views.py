from django.shortcuts import render

def error_404(request):
    return render(request, '404.html')

# def home(request):
#     return render_to_response('home/home.html')



