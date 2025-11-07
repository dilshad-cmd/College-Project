from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from Teachers.models import *
from datetime import datetime
from django.utils import timezone

# # Create your views here.
def login(request):
   return render(request, 'login.html')

def logindatasfunc(request):
      user = request.POST.get('uname')
      psw = request.POST.get('upsw')
      checklogin = logindata.objects.filter(uname=user, upsw=psw)
      if checklogin.exists():
         checklogin = logindata.objects.get(uname=user, upsw=psw)
         request.session['lid'] = checklogin.id
         if checklogin.type == 'student':
            return HttpResponse ('''<script>alert("Open Student Home.!");window.location='/studenthome/'</script>''')
         if checklogin.type == 'staff':
            return HttpResponse ('''<script>alert("Open Staff Home.!");window.location='/staff/'</script>''')
      else:
         return HttpResponse ('''<script>alert("you didnt register.Please Signup!");window.location=''</script>''')


      
   # return redirect('login/')
def create_students(request):
   subjects = subject.objects.all()
   return render(request, 'addstudent.html', {'subjects': subjects})

def readstudents(request):
   if request.method == "POST":

      sfname = request.POST.get('first_name')
      slname = request.POST.get('last_name')
      smail = request.POST.get('email')
      scontact = request.POST.get('contact')
      sdateob = request.POST.get('dob')
      sgender = request.POST.get('gender')
      saddress = request.POST.get('address')
      scty = request.POST.get('city')
      sstate = request.POST.get('state')
      spost = request.POST.get('post')
      spsw = request.POST.get('upsw')
      ssubject = request.POST.get('std_sub','').strip()

      selected_subject = subject.objects.get(id=ssubject)

      loginstdd = logindata.objects.create(
         uname = smail,
         upsw = spsw,
         type = 'student'
      )
      

      save_students = students.objects.create(
         first_name = sfname,
         last_name = slname,
         email = smail,
         contact = scontact,
         dob = sdateob,
         gender = sgender,
         address = saddress,
         city = scty,
         state = sstate,
         post = spost,
         std_sub = selected_subject,
         loginstd=loginstdd,
      )
      save_students.save()

   return HttpResponse ('''<script>alert("Students Registration Is Successfully Completed.!");window.location='/admin/Teachers/students/'</script>''')

def staff(request):
   lid = request.session.get('lid') 
   gg=Clg_teachers.objects.get(stafflogin_id=lid).name
   if not lid:
      return redirect('logindatasfunc')

   checklogin = logindata.objects.get(id=lid)
   return render(request, 'user_staff.html',{'checklogin':gg})

def allstudents(request):
   data = students.objects.all()
   return render(request, 'Students.html',{'data':data})

def myschedule(request):
   nn=request.session['lid']
   # print(nn)
   schrecord = Set_schedule.objects.filter(staffs__stafflogin_id=nn)
   if request.method == "POST":
     
      sub_id = request.POST.get('sub')
      if schrecord:
         if nn:
               schrecord.staffs = Clg_teachers.objects.get(stafflogin_id=nn)
         if sub_id:
            schrecord.sub = subject.objects.get(id=sub_id)

         schrecord.weekly_days = request.POST.get('weekly_days')
         schrecord.save()

   data = Set_schedule.objects.filter(staffs__stafflogin_id=nn).order_by('period')
   weekday = [day[0] for day in Set_schedule.DAY_CHOICES]

   return render (request,'staffscheduletable.html', {'data':data, 'weekday':weekday})
      
def addnotestaff(request):
      lid = request.session.get('lid')
      if not lid:
         return redirect('logindatasfunc')
      staff = Clg_teachers.objects.get(stafflogin_id=lid)
      assigned_subs = staff.sub.all()
      return render (request, 'note.html',{"assigned_subs":assigned_subs})

def addnotefunc(request):
   lid = request.session.get('lid')  # logged-in staff id from login
   if not lid:
        return redirect('logindatasfunc')
   
   staff = Clg_teachers.objects.get(stafflogin_id=lid)
   # assigned_subs = staff.sub.all()


   if request.method == "POST":
      snote = request.POST.get('addnote')
      sub_id = request.POST.get('sub')
      print(sub_id)

      print("POST sub_id:", sub_id)
      if not sub_id:
            return HttpResponse('''<script>alert("Pls select a course..!"); </script>''')
      try:
          subject_obj = subject.objects.get(id=sub_id)
      except subject.DoesNotExist:
          return HttpResponse('''<script>alert("Invalid course selected..!"); window.history.back();</script>''')
      

      savednote = notes(
      addnote = snote,
      sub = subject_obj
      # sub = assigned_sub
      )
      savednote.save()
      return HttpResponse('''<script>alert("shortnote added succesfully..!"); </script>''')
   return redirect('addnotestaff')

def studenthome(request):
   lid = request.session.get('lid')
   if not lid:
      return redirect('logindatasfunc')
   std_obj = students.objects.get(loginstd_id=lid)
   std_name = std_obj.first_name
      
      # std_idntfy =  request.post.get('std_sub')
      # sub_id = subject.objects.get(id = std_idntfy)
   course = std_obj.std_sub

   notes_by_course = notes.objects.filter(sub=course).order_by('-created_at')
   
   return render (request, 'stdnthomepage.html', {'stdname':std_name, 'notes':notes_by_course, 'course':course})

def staffnoteditfunc(request):
    lid = request.session.get('lid')
    if not lid:
         return redirect('logindatasfunc')
    staff = Clg_teachers.objects.get(stafflogin_id=lid)
    assigned_sub = staff.sub.all()
    notes_by_course = notes.objects.filter(sub__in=assigned_sub)
    return render  (request, 'staffallnotetable.html', {'staff':staff, 'assigned_sub':assigned_sub, 'notes':notes_by_course}) 

def staffnotedltfunc (request,id):
    mynotes = notes.objects.get(pk=id)
    mynotes.delete()
    return redirect('/staffnoteditfunc/')
def attendanceform (request):
    lid = request.session.get('lid')
    if not lid:
        return redirect('logindatasfunc')
    teacher = Clg_teachers.objects.get(stafflogin_id=lid)
    subj = teacher.sub.all()

    selected_sub_id = request.GET.get('subject_id')
    student = students.objects.none()

    if selected_sub_id:
        student = students.objects.filter(std_sub_id = selected_sub_id)
    context = {
        'teacher':teacher,
        'subjects':subj,
        'students':student,
        'selected_sub_id':selected_sub_id,
        'today': timezone.now().date()
    }
    
    return render (request, 'attendanceform.html',context)
def save_attendance(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        date = request.POST.get('date')
        present_ids = request.POST.getlist('present_ids')
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        subj_obj = get_object_or_404(subject,id=subject_id)
        student_at = students.objects.filter(std_sub = subj_obj)

        for stud in student_at:
            status = 'present' if str(stud.id) in present_ids else 'absent'
            attendance.objects.update_or_create(
                student = stud,
                subj = subj_obj,
                date = date_obj,
                defaults={'status':status}
            )
        return redirect ('attendanceform')
        
def readattendance(request):
    lid = request.session.get('lid')
    if not lid:
        return redirect('logindatasfunc')
    teacher = Clg_teachers.objects.get(stafflogin_id=lid) 
    subje = teacher.sub.all()
    subject_id = request.GET.get('subject_id')
    data = attendance.objects.none()
    if subject_id:
         subject_fil= get_object_or_404(subject, id=subject_id)
         data = attendance.objects.filter(subj = subject_fil)
    context = {
        'teacher':teacher,
        'subje':subje,
        'data':data,
    }
    return render(request, 'attendancetable.html', context)
# return render(request, 'attendancetable.html', {'data':data, 'subje':subje})

def studnetatt (request):
    lid = request.session.get('lid')
    if not lid:
        return ('logindatasfunc')
    student_log = students.objects.get(loginstd=lid)
    subject_id = request.GET.get('subject_id')
    
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    fl_student = attendance.objects.filter(student = student_log).order_by('-date')
    if subject_id and subject_id.isdigit():
        fl_student = fl_student.filter(subj_id=int(subject_id))
        
    if date_from:
        try:
            dt_from = datetime.strptime(date_from, "%Y-%m-%d")
            fl_student = fl_student.filter(date__date__lte=dt_from.date())
        except ValueError:
            pass
        
    if date_to:
        try:
            dt_to = datetime.strptime(date_to, "%Y-%m-%d")
            fl_student = fl_student.filter(date__date__lte=dt_to.date())
        except ValueError:
            pass
        
    
    context = {
        'student' : student_log,
        'attendance_list':  fl_student,
        'selected_sub' : subject_id,
        'date_from' : date_from,
        'date_to' : date_to
    }
    

    return render (request, 'attendancetableforstudents.html', context)