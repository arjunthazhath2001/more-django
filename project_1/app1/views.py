from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Room,Topic,Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms  import RoomForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

# rooms=[
#     {'id':1, 'name':'arjun', 'age':20},
#     {'id':2, 'name':'anjali','age':20},
#     {'id':3, 'name':'jaya','age':10} 
# ]



def loginPage(request):
    page='login'
    
    
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="POST":
        username= request.POST.get('username').lower()
        password= request.POST.get('password')
        
        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        
        
        user= authenticate(request, username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'User not authenticated')
            
        
        
    context={'page':page}
    return render(request,'app1/login_register.html',context)



def logoutUser(request):
    logout(request)
    return redirect("home")



def registerPage(request):
    form= UserCreationForm()
    
    if request.method=="POST":
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    return render(request, 'app1/login_register.html',{'form': form})



def home(request):
    q= request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms= Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q)| Q(desc__icontains=q))
    
    topics= Topic.objects.all()
        
    room_count= rooms.count()

    room_messages= Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context= {'rooms':rooms, 'topics': topics, 'room_count':room_count, 'room_messages': room_messages}
    return render(request,'app1/home.html', context)

def room(request,pk):
    room= Room.objects.get(id=pk)
    room_messages= room.message_set.all()
    participants= room.participants.all()
    if request.method=="POST":
        message= Message.objects.create(
            user= request.user,
            room= room,
            body= request.POST.get('body')
        )
        
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    
    context= {'room':room, 'room_messages': room_messages, 'participants':participants}
    return render(request,'app1/room.html',context)


def userProfile(request,pk):
    user= User.objects.get(id=pk)
    rooms= user.room_set.all()
    
    room_message= user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user, 'rooms': rooms, 'room_messages': room_message,'topics':topics}
    return render(request,'app1/profile.html',context)





@login_required(login_url="login")
def createRoom(request):
        
    form = RoomForm()
    
    
    if request.method=="POST": #if its a post request
        form= RoomForm(request.POST)  
        # send the data to check whether it matches the form schema aka db schema
        if form.is_valid():  #if the schema aligns with info entered by user
            room= form.save(commit=False) #save the form aka form data on the "ROOM" Model, because this form inherited from the ROOM model
            room.host= request.user
            room.save()
            return redirect('home')  #then we redirect the user back to home page
        
    context={'form':form}
    return render(request,'app1/room_form.html',context)


@login_required(login_url="login")

def updateRoom(request,pk):
    room= Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    
    if request.user != room.host:
        return HttpResponse('you are not allowed')
    
    
    context={'form':form}
    if request.method=="POST": #if its a post request
        form= RoomForm(request.POST, instance=room)  
        # send the data to check whether it matches the form schema aka db schema
        if form.is_valid():  #if the schema aligns with info entered by user
            form.save() #save the form aka form data on the "ROOM" Model, because this form inherited from the ROOM model
            return redirect('home')  #then we redirect the user back to home page
        
    return render(request, 'app1/room_form.html',context)


@login_required(login_url="login")
def deleteRoom(request,pk):
    room= Room.objects.get(id=pk)
    
    
    if request.user != room.host:
        return HttpResponse('you are not allowed')
    
    if request.method=="POST":
        room.delete()
        return redirect('home')
        
    return render(request,'app1/delete.html', {'obj':room})


@login_required(login_url="login")
def deleteMessage(request,pk):
    message= Message.objects.get(id=pk)
    
    
    if request.user != message.user:
        return HttpResponse('you are not allowed')
    
    if request.method=="POST":
        
        message.delete()
        return redirect('home')
        
    return render(request,'app1/delete.html', {'obj':message})

    