from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message,OnGoingProjects
from django.contrib import messages
from braces.views import SuperuserRequiredMixin,UserPassesTestMixin
from freelancer.models import Requirement
from chat.models import Room

@login_required
def index(request):
    current_user=request.user
    users=User.objects.exclude(username=current_user).all()
    context={'users':users,'current_user':current_user}
    return render(request,'chat/index.html',context)

@login_required
def chat(request,user1,user2):
    return render(request,'chat/room.html',{'user1':user1,'user2':user2})


class MessageDeleteView(LoginRequiredMixin,DeleteView):
    model = Message
    success_url = '/chat/'
    template_name='chat/message_confirm_delete.html'
    def post(self, request, *args, **kwargs):
        self.to_delete = self.request.POST.get('todelete')
        if  self.to_delete:
            user1=self.request['kwargs']['user1']
            author=user1
            user2=self.request['kwargs']['user2']
            ar=[user1,user2]
            ar=sorted(ar)
            user1=ar[0]
            user2=ar[1]
            messages=Message.objects.filter(sort_str=f'{user1}_{user2}').all()
            if author == messages.first().author:
                messages.delete()
                messages.success(request,f'successfully deleted chat: of {user1} and {user2}')
                return redirect('chat-index')
        else:
            return self.get(self, *args, **kwargs)

@login_required
def message_delete(request,user1,user2):
    if request.method=='POST':
        to_delete = request.POST.get('todelete')
        if  to_delete:
            author=user1
            ar=[user1,user2]
            ar=sorted(ar)
            user1=ar[0]
            user2=ar[1]
            Message.objects.filter(sort_str=f'{user1}_{user2}').all().delete()
            messages.success(request,f'successfully deleted chat: of {user1} and {user2}')
            return redirect('chat-index')
    else:
        return render(request,'chat/message_confirm_delete.html')

@login_required
def room(request,room_name,creator):
    return render(request,'chat/freelancer_room.html',{'room_name':room_name,'creator':creator})

@login_required
def freelancer_chat(request,room_name,performer):
    provider=request.user.username
    projects=OnGoingProjects.objects.filter(room_name=room_name)
    if not projects:
        provider=User.objects.get(username=provider)
        performer=User.objects.get(username=performer)
        OnGoingProjects.objects.create(room_name=room_name,provider=provider,performer=performer)
    
    #Deleting the requirement object
    # requirement = Requirement.objects.get(title=room_name)
    try:
        requirement = Requirement.objects.get(title=room_name)
        if requirement:
            Room.objects.filter(room_name=requirement.title).all().delete()
            requirement.delete()
    except:
        pass

    context={'room_name':room_name,'performer':performer}
    return render(request,'chat/freelancer_chat.html',context)


@login_required
def freelancer_confirm(request,room_name,performer):
    if request.method == 'POST':
        return redirect('/freelancer/requirement/'+ room_name +'/'+ performer +'/chat/')
    else:
        context={'room_name':room_name,'provider':request.user.username,'performer':performer}
        return render(request,'chat/freelancer_confirm.html',context)








