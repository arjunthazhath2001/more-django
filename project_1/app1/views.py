from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# rooms=[
#     {'id':1, 'name':'arjun', 'age':20},
#     {'id':2, 'name':'anjali','age':20},
#     {'id':3, 'name':'jaya','age':10} 
# ]

def home(request):
    rooms= Room.objects.all()
    context= {'rooms':rooms}
    return render(request,'app1/home.html', context)

def room(request,pk):
    room= Room.objects.get(id=pk)
    context= {'room':room}
    return render(request,'app1/room.html',context)

