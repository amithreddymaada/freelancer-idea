from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .models import Requirement
from braces.views import SuperuserRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from chat.models import Room
from django.contrib.auth.models import User
from chat.models import OnGoingProjects,FreelancerChat
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'freelancer/base.html')

class RequirementListView(ListView):
    model = Requirement
    template_name = 'freelancer/home.html'

class RequirementCreateView(SuperuserRequiredMixin,CreateView):
    model=Requirement
    fields=['title','content']
    success_url='/freelancer'

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class RequirementUpdateView(SuperuserRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Requirement
    fields=['title','content']
    success_url='/freelancer'

    def form_valid(self,form):
        form.instance.author=self.request.user
        messages.success(self.request,f'successfully update the requirement:{form.instance.title}')
        return super().form_valid(form)
    
    def test_func(self,*args):
        requirement=self.get_object()
        if requirement.author == self.request.user:
            return True
        else:
            return False
        
class RequirementDeleteView(SuperuserRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Requirement
    success_url='/freelancer'
    def test_func(self,*args):
        requirement=self.get_object()
        if requirement.author == self.request.user:
            return True
        else:
            return False

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            requirement=self.get_object()
            Room.objects.filter(room_name=requirement.title).all().delete()
            requirement.delete()
            messages.success(request,f'Succesfully deleted the post')
            return redirect('freelancer-list')
        else:
            return self.get(request,*args,**kwargs)

@login_required
def on_going_projects(request,username):
    user=User.objects.get(username=username)
    if user.is_superuser:
        projects=OnGoingProjects.objects.filter(provider=user)
    else:
        projects = OnGoingProjects.objects.filter(performer=user)
    
    return render(request,'freelancer/projects.html',{'projects':projects})

def complete_project(request,room_name,performer):
    if request.user.is_superuser:
        OnGoingProjects.objects.filter(room_name=room_name).all().delete()
        FreelancerChat.objects.filter(room_name=room_name).all().delete()
        messages.success(request,f'successfully completed the project {room_name}')
        return redirect('freelancer-list')
    else:
        messages.error(request,f'You dont have permission to delete project : {room_name}')
        return redirect('freelancer-list')

def confirm_complete_project(request,room_name,performer):
    if request.method == 'POST':
        return redirect('/freelancer/requirement/'+room_name+'/'+performer+'/delete-project/complete/')
    else:
        context={'room_name':room_name,'performer':performer}
        return render(request,'freelancer/confirm_complete_project.html',context)
    




