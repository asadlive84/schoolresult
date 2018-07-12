from django.db import models
from django.contrib.auth.models import AbstractUser
from .grade_sheet import SubjectGrade, SubjectGradePoint
from django.utils import timezone

from django.db.models import Avg, Count, Min, Sum


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
        return self.subject_type+' Code: '+self.subject_code+' - '+self.subject_name+' | class: '+self.subjet_class

    class Meta:
        verbose_name = ("Subject")
        verbose_name_plural = ("Subject")

class StudentInfo(StdCommon):
    

    

    std_name = models.CharField('Student Name',max_length=100, help_text='Type only student Full Name like as Nazmul Islam or Nazrul Islam')
    std_class = models.CharField('Student Class',max_length=2, choices=STD_CLASS, default=6, help_text='Select a class')
    std_roll = models.IntegerField('Roll Number',help_text='Type Student Roll Number (Only Number)')
    std_group=models.CharField('Group', choices=STD_GROUP, max_length=1, default='G')
    std_gender=models.CharField('Gender', max_length=10, choices=STD_GENDER, default='MALE')
    std_subjects = models.ManyToManyField(StdSubject)


    std_total_marks = models.FloatField('Total Marks', default=0, blank=True, null=True)

    std_gpa = models.CharField('GPA', max_length=50,default='F', blank=True, null=True)

    std_grade_point_total_sum=models.FloatField('Total Avg Number per Subject', blank=True, null=True) # toal grade point sum

    std_grade_point_total_subject_avg = models.FloatField(
        'Total GPA', blank=True, null=True) #avg gradepoint

    std_fail_subject=models.IntegerField('Fail Subject', blank=True, null=True)


    rank=models.IntegerField('Student Rank in School',default=0)
    

    
    def __str__(self):
        return self.std_name

    class Meta:
            verbose_name = ("Student Detail")
            verbose_name_plural = ("Student Detail's")
            ordering = ['std_roll']


    def total_marks_sum(self):
        std_id = self.id
        x = Marks.objects.filter(std_name=std_id).aggregate(
            total_number=Sum('subject_marks')).get('total_number', 0)

        return x


    def save(self, *args, **kwargs):
        
        std_id = self.id
        fail_sub = 0
        std_result='Pass'

        total_number = Marks.objects.filter(std_name=std_id).aggregate(
            total_number=Sum('subject_marks')).get('total_number', 0)

        subject_grade = ((Marks.objects.filter(std_name=std_id, subject_gradepoint__gte=1).aggregate(sp=Sum('subject_gradepoint')).get('sp', 0)))

        

        self.std_total_marks = total_number

        if subject_grade is None:
            subject_grade=0
        

        self.std_grade_point_total_sum = subject_grade

        subject_grade_f = Marks.objects.filter(std_name=std_id, subject_name__subject_type__startswith='R')


        
            


        
        for i in subject_grade_f:
            
            if 'F' in i.subject_gpa:
                fail_sub = fail_sub+1
                
            std_result = 'Fail ' +str(fail_sub)+' Subject'

        self.std_gpa = std_result

        self.std_fail_subject=fail_sub

        if fail_sub >=1:
            self.std_grade_point_total_subject_avg=0
            
        else:
            if self.std_class == '6' or self.std_class == '7':
                self.std_grade_point_total_subject_avg = (subject_grade/7)
            elif self.std_class == '8':
                self.std_grade_point_total_subject_avg = (subject_grade/7)

            elif self.std_class == '9' or self.std_class == '10':
                self.std_grade_point_total_subject_avg = (subject_grade/9)
        
        
       
        super(StudentInfo, self).save(*args, **kwargs) # Call the real save() method

        

        



    


class Marks(StdCommon):
    std_name = models.ForeignKey(
        StudentInfo, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(StdSubject, on_delete=models.CASCADE)
    subject_marks=models.DecimalField(max_digits=5, decimal_places=2, help_text='Please give proper number')

    subject_gradepoint=models.DecimalField('Grade Point', max_digits=3, decimal_places=1, blank=True, null=True, help_text="Please keep blank")
    subject_gpa = models.CharField('Subject GPA', max_length=5, blank=True, null=True, help_text="Please keep blank")
    
   


    def __str__(self):
        return self.std_name.std_name+' Class: '+str(self.std_name.std_class)+' Roll: '+str(self.std_name.std_roll) +' ' + self.subject_name.subject_name +' '+str(self.subject_marks)

    class Meta:
        verbose_name = ("Mark Details")
        verbose_name_plural = ("Result Sheet Details")
        ordering = ['subject_name']

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




class Rank(models.Model):
    std = models.ForeignKey(StudentInfo, related_name='std', on_delete=models.CASCADE)
    
    total_marks = models.DecimalField(
        max_digits=5, decimal_places=2, help_text='Please give proper number', default=0)
    total_gpa = models.DecimalField(
        max_digits=5, decimal_places=2, help_text='Please give proper number', default=0)
    class_rank = models.IntegerField(default=0)
    school_rank=models.IntegerField('All School Rank', default=0)



    def __str__(self):
        return 'Name: %s |  Marks: %s | Class Rank %s | School Rank %s' % (self.std, self.total_marks, self.class_rank, self.school_rank)

    class Meta:
            verbose_name = ("Rank")
            verbose_name_plural = ("Rank")
            ordering = ['class_rank']
