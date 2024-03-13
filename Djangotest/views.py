from django.shortcuts import render

def home_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request, 'HTML/home.html', context)

def index_view(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/index/index.html',context)

def admin_panel(request):
    context = {}  # You can pass context data to the template if needed
    return render(request,'HTML/admin_panel/admin_panel.html', context)
