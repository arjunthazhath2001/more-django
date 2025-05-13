from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic
from .forms  import RoomForm

# rooms=[
#     {'id':1, 'name':'arjun', 'age':20},
#     {'id':2, 'name':'anjali','age':20},
#     {'id':3, 'name':'jaya','age':10} 
# ]

def home(request):
    q= request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms= Room.objects.filter(topic__name__icontains=q)
    
    topics= Topic.objects.all()
    context= {'rooms':rooms, 'topics': topics}
    return render(request,'app1/home.html', context)

def room(request,pk):
    room= Room.objects.get(id=pk)
    context= {'room':room}
    return render(request,'app1/room.html',context)


def createRoom(request):
        
    form = RoomForm()
    
    
    if request.method=="POST": #if its a post request
        form= RoomForm(request.POST)  
        # send the data to check whether it matches the form schema aka db schema
        if form.is_valid():  #if the schema aligns with info entered by user
            form.save() #save the form aka form data on the "ROOM" Model, because this form inherited from the ROOM model
            return redirect('home')  #then we redirect the user back to home page
        
    context={'form':form}
    return render(request,'app1/room_form.html',context)


def updateRoom(request,pk):
    room= Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    context={'form':form}
    if request.method=="POST": #if its a post request
        form= RoomForm(request.POST, instance=room)  
        # send the data to check whether it matches the form schema aka db schema
        if form.is_valid():  #if the schema aligns with info entered by user
            form.save() #save the form aka form data on the "ROOM" Model, because this form inherited from the ROOM model
            return redirect('home')  #then we redirect the user back to home page
        
    return render(request, 'app1/room_form.html',context)


def deleteRoom(request,pk):
    room= Room.objects.get(id=pk)
    
    if request.method=="POST":
        room.delete()
        return redirect('home')
        
    return render(request,'app1/delete.html', {'obj':room})

    