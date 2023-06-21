from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_task/', views.add_task, name='add_task'),
    path('preview_task/<int:id>/', views.preview_task, name='preview_task'),
    path('end_task/<int:id>/', views.end_task, name='end_task'),
    path('edit_task/<int:id>/', views.edit_task, name='edit_task'),
    path('pdf_view/<str:path>/', views.pdf_view, name='pdf_view'),
    ################################################################
    path('task_notes/<int:id>/',views.task_notes,name='task_notes'),
    path('add_note/<int:id>/',views.add_note,name='add_note'),
    path('delete_task/<int:id>/',views.delete_task,name='delete_task'),
]
