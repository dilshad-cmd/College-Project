from django.contrib import admin
from django.urls import path

from Teachers import views

urlpatterns =[

    path('login/',views.login,name='login'),
    path('logindatasfunc/,',views.logindatasfunc,name='logindatasfunc'),
    path('addstd/', views.create_students,name='create_students'),
    path('readstudents/', views.readstudents, name='readstudents'),
    path('staff/',views.staff,name='staff'),
    path('allstudents/',views.allstudents,name='allstudents'),
    path('addnotestaff/',views.addnotestaff,name='addnotestaff'),
    path('addnotefunc/',views.addnotefunc, name='addnotefunc'),
    path('myschedule/',views.myschedule,name='myschedule'),
    path('studenthome/',views.studenthome,name='studenthome'),
    path('staffnoteditfunc/', views.staffnoteditfunc, name='staffnoteditfunc'),
    path('staffnotedltfunc/<int:id>/',views.staffnotedltfunc,name='staffnotedltfunc'),
    path('attendanceform/',views.attendanceform,name='attendanceform'),
    path('save_attendance/',views.save_attendance,name='save_attendance'),
    path('readattendance/',views.readattendance,name='readattendance'),
    path('studnetatt/',views.studnetatt,name='studnetatt')
    
]
