from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('This is a placeholder to display all blogs')

def new(request):
    return HttpResponse('Placeholder to display a new form to create a new blog')

def create(request):
    return redirect('/')

def number(request, number):
    return HttpResponse('This is a placeholder to display blog ' + number)

def edit(request, number):
    return HttpResponse('This is a placeholder to edit blog  ' + number)

def destroy(request, number):
    return redirect('/')