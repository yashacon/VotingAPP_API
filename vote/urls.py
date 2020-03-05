from django.urls import path

from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
    path('',views.login,name='Login'),
    path('register',views.FileUploadView.as_view(),name='Register'),
    path('logout',views.logout,name='Logout'),
    path('vote',views.vote,name='Vote'),
    path('vote/<str:title>',views.voting,name='Voting'),
    path('add',views.AddItem,name='AddItem')
]
