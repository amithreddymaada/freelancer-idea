from django.urls import path
from . import views 
from chat import views as chat_views

urlpatterns=[
    path('',views.RequirementListView.as_view(),name='freelancer-list'),
    path('requirement/create/',views.RequirementCreateView.as_view(),name='freelancer-create'),
    path('requirement/<int:pk>/update/',views.RequirementUpdateView.as_view(),name='freelancer-update'),
    path('requirement/<int:pk>/delete/',views.RequirementDeleteView.as_view(),name='freelancer-delete'),
    path('requirement/<str:room_name>/<str:creator>/room/',chat_views.room,name='freelancer-room'),
    path('requirement/<str:room_name>/<str:performer>/chat/',chat_views.freelancer_chat,name='freelancer-chat'),
    path('requirement/<str:room_name>/<str:performer>/confirm/',chat_views.freelancer_confirm,name='freelancer-confirm'),
    path('requirement/<str:username>/',views.on_going_projects,name='freelancer-on-going-projects'),
    path('requirement/<str:room_name>/<str:performer>/delete-project/complete/',views.complete_project,name='freelancer-complete'),
    path('requirement/<str:room_name>/<str:performer>/delete-project/confirm/',views.confirm_complete_project,name='freelancer-confirm-complete'),
]