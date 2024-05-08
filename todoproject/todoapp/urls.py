from . import views
from django.urls import path

app_name = 'todoapp'

urlpatterns = [

    path('add/<int:id>/', views.add, name='add'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('update/<int:id>/', views.update, name='update'),
    
    path('addproject/<int:user_id>/', views.addproject, name='addproject'),
    path('deleteproject/<int:id>/', views.deleteproject, name='deleteproject'),
    path('updateproject/<int:id>/', views.updateproject, name='updateproject'),
    path('updateprojectheading/<int:id>/', views.updateprojectheading, name='updateprojectheading'),

    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('export_summary/<int:project_id>/', views.export_summary, name='export_summary'),
]
