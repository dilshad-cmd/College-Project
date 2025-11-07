from django import forms
from django.contrib import admin
from Teachers.models import Clg_teachers, Set_schedule, subject, students, logindata
# Register your models here.
class Clg_teachersAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')
admin.site.register(Clg_teachers,Clg_teachersAdmin)
# ---------------------------------------------------------------------------------------------------------
class SetScheduleForm(forms.ModelForm):
    class meta:
        model = Set_schedule
        fields = '__all__'

    def __init__ (self, *args, **kwargs):
        super(). __init__(*args, **kwargs)
        if 'staffs' in self.data:
            try:
                staff_id = int(self.data.get('staffs'))
                staff = Clg_teachers.objects.get(id=staff_id)
                self.fields['sub'].queryset = staff.sub.all()
            except (ValueError,Clg_teachers.DoesNotExist):
                self.fields['sub'].queryset = subject.objects.none()
        else:
            self.fields['sub'].queryset = subject.objects.all()

class TeachersAdmin(admin.ModelAdmin):
    form = SetScheduleForm
    list_display = ('staffs', 'sub', 'period', 'weekly_days')
    list_filter = ('weekly_days', 'staffs')
    search_fields = ('sub',)


admin.site.register(Set_schedule,TeachersAdmin,)
# -------------------------------------------------------------------------------------------------------------
admin.site.register(subject,)
# -------------------------------------------------------------------------------------------------------------
class students_Admin(admin.ModelAdmin):
    list_display = ('first_name', 'email','contact', 'state', 'date_created' )
admin.site.register(students,students_Admin)
# ------------------------------------------------------------------------------------------------------------------
class loginAdmin(admin.ModelAdmin):
    list_display = ('uname','upsw')

admin.site.register(logindata,loginAdmin)