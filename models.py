from django.db import models
from  django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_delete
# Create your models here.
    
class logindata(models.Model):
    uname = models.CharField(max_length=155)
    upsw = models.CharField(max_length=155)
    type = models.CharField(max_length=155)
    def __str__(self):
        return self.uname

class subject(models.Model):
    Add_new_subject = models.CharField(max_length=50)
    def __str__(self):
        return self.Add_new_subject
    
class Clg_teachers(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, unique=True)
    contact = models.CharField(max_length=13, unique=True)
    stafflogin = models.ForeignKey(logindata, on_delete=models.CASCADE)
    sub = models.ManyToManyField(subject)

    def __str__(self):
        return self.name
    

class Set_schedule(models.Model):
    DAY_CHOICES=[
        ('Monday', 'MON'),
        ('Tuesday', 'TUE'),
        ('Wednesday', 'WED'),
        ('Thursday', 'THURS'),
        ('FRIDAY', 'FRI'),
    ]


    PERIODS_CHOICES=[
        ('1','1st'),
        ('2','2nd'),
        ('3','3rd'),
        ('4','4th'),
        ('5','5th')
    ]
    staffs = models.ForeignKey(Clg_teachers, on_delete=models.CASCADE)
    weekly_days=models.CharField(max_length=15, choices=DAY_CHOICES)
    sub = models.ForeignKey(subject, on_delete=models.CASCADE)
    period = models.CharField(max_length=5, choices=PERIODS_CHOICES)

    def __str__(self):
        return f"schedule of{self.staffs.name}"
    
    @property
    def staffs_name(self):
        return self.staffs.name

class students(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    contact = models.CharField(max_length=13)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    post = models.IntegerField()
    std_sub = models.ForeignKey(subject, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    loginstd = models.ForeignKey(logindata, on_delete=models.CASCADE, null = False, blank=False)


    def __str__(self):
        return f"{self.first_name}{self.last_name}"

@receiver(post_delete, sender=students)
def delete_related_login(sender, instance, **kwargs):
        if instance.loginstd:
            instance.loginstd.delete()

        # if instance.loginstd:
        #     instance.loginstd.delete()

class notes (models.Model):
        addnote = models.CharField(max_length=2000)
        sub = models.ForeignKey(subject, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)

class attendance (models.Model):
     student = models.ForeignKey(students, on_delete=models.CASCADE)
     subj = models.ForeignKey(subject, on_delete=models.CASCADE)
     date = models.DateField()
     status = models.CharField (max_length=10,choices=[('present','present'),('absent','absent')])

     class Meta:
        unique_together = ('student', 'subj', 'date')

     def __str__(self):
        return f"{self.student.first_name} - {self.subj} ({self.date})"