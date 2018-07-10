from django.db import models
from django.contrib.auth.models import AbstractUser
from .grade_sheet import SubjectGrade, SubjectGradePoint
from django.utils import timezone


STD_CLASS = (
    ('6', 'Six'),
    ('7', 'Seven'),
    ('8', 'Eight'),
    ('9', 'Nine'),
    ('10', 'Ten'),
)


STD_GENDER = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
)

STD_GROUP = (
        ('S', 'Science'),
        ('B', 'Business Studies'),
        ('H', 'Humatics'),
        ('G', 'General')
)


REGULAR = 'R'
OPTIONAL = 'O'

SUBJECT_TYPE_CHOICE = (
        (REGULAR, 'REGULAR'),
        (OPTIONAL, 'OPTIONAL')
)




class CustomUser(AbstractUser):
    name=models.CharField('Full Name',max_length=100)



class StdCommon(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    


class StdSubject(StdCommon):
    

    subject_name = models.CharField('Subject Name', max_length=100)
    subject_code=models.CharField('Subject Code', max_length=10)
    subjet_class = models.CharField(
        'Subject Class', max_length=2, choices=STD_CLASS, default='6')
    subject_type = models.CharField(
        'Subject Type', max_length=1, default=REGULAR, choices=SUBJECT_TYPE_CHOICE)
    subject_full_marks = models.DecimalField(
        'Full Marks', max_digits=5, decimal_places=2, default=100)
    subject_pass_marks = models.DecimalField(
        'Pass Marks', max_digits=5, decimal_places=2)
    

    def __str__(self):
        return 'Code: '+self.subject_code+' - '+self.subject_name+' | class: '+self.subjet_class


class StudentInfo(StdCommon):
    

    

    std_name = models.CharField('Student Name',max_length=100, help_text='Type only student Full Name like as Nazmul Islam or Nazrul Islam')
    std_class = models.CharField('Student Class',max_length=2, choices=STD_CLASS, default=6, help_text='Select a class')
    std_roll = models.IntegerField('Roll Number',help_text='Type Student Roll Number (Only Number)')
    std_group=models.CharField('Group', choices=STD_GROUP, max_length=1, default='G')
    std_gender=models.CharField('Gender', max_length=10, choices=STD_GENDER, default='MALE')
    std_subjects = models.ManyToManyField(StdSubject)


    std_total_marks = models.FloatField('Total Marks', default=0)
    std_gpa = models.CharField('GPA', max_length=10,default='F')

    
    def __str__(self):
        return self.std_name


    


class Marks(StdCommon):
    std_name = models.ForeignKey(
        StudentInfo, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(StdSubject, on_delete=models.CASCADE)
    subject_marks=models.DecimalField(max_digits=5, decimal_places=2, help_text='Please give proper number')

    subject_gradepoint=models.DecimalField('Grade Point', max_digits=3, decimal_places=1, blank=True, null=True, help_text="Please keep blank")
    subject_gpa = models.CharField('Subject GPA', max_length=5, blank=True, null=True, help_text="Please keep blank")
    std_result=models.FloatField(blank=True, null=True)
   


    def __str__(self):
        return self.std_name.std_name+' Class: '+str(self.std_name.std_class)+' Roll: '+str(self.std_name.std_roll) +' ' + self.subject_name.subject_name +' '+str(self.subject_marks)



    def subject_grade(self):
        grade = SubjectGrade(self.subject_marks,self.subject_name.subject_full_marks).subgrade()
        return grade

    def subject_grade_point(self):
        grade = SubjectGradePoint( self.subject_marks, self.subject_name.subject_full_marks).subgrade()
        return grade


    def save(self, *args, **kwargs):
        grade_point = SubjectGradePoint(self.subject_marks, self.subject_name.subject_full_marks).subgrade()
        gpa = SubjectGrade(self.subject_marks,self.subject_name.subject_full_marks).subgrade()

        if self.subject_name.subject_type=='O':
            if self.subject_marks >= ((self.subject_name.subject_full_marks/100)*50) and self.subject_marks <= self.subject_name.subject_full_marks:
                subject_opt_grade_point = grade_point-2

                self.subject_gradepoint = subject_opt_grade_point
                self.subject_gpa = gpa
            elif self.subject_marks >= ((self.subject_name.subject_full_marks/100)*33) and self.subject_marks < ((self.subject_name.subject_full_marks/100)*50):
                self.subject_gradepoint = 0
                self.subject_gpa=gpa

            elif self.subject_marks < ((self.subject_name.subject_full_marks/100)*33):
                self.subject_gradepoint = 0
                self.subject_gpa = gpa

                
        elif self.subject_name.subject_type=='R':
            self.subject_gradepoint = grade_point
            self.subject_gpa = gpa

        super().save(*args, **kwargs)


class ShortStudentDetails(StdCommon):
    std_id=models.CharField(max_length=400)

    std_name = models.CharField('Student Name', max_length=100,
                                help_text='Type only student Full Name like as Nazmul Islam or Nazrul Islam')
    std_class = models.CharField('Student Class', max_length=50,)
    std_roll = models.IntegerField('Roll Number', help_text='Type Student Roll Number (Only Number)')
    std_group = models.CharField('Group',  max_length=50)
    std_gender = models.CharField(
        'Gender', max_length=50 )
    
    std_total_marks=models.FloatField('Total Marks', default=0)
    std_gpa=models.CharField('GPA', max_length=10)

    def __str__(self):
        return self.std_name
