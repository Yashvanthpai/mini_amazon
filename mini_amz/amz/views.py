from django.shortcuts import render

def index(request):
    return render(request,'index.html',{'xyz':'yes'})

def one(request):
    return render(request,'one.html',{'xyz':''})