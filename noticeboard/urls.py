from django.urls import path
from . import views

app_name = 'noticeboard'

urlpatterns = [
    path('', views.noticeboard_view, name='main'),
    path('AddNotice',views.add_Notice,name='add_notice'),
    path('mynotice',views.my_Notices,name='my_notice'),
    path('delete/<slug:slug>',views.delete_Notice,name='delete_notice'),
    path('edit/<slug:slug>',views.edit_Notice,name='edit_notice'),


]