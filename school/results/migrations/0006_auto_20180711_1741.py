# Generated by Django 2.0.6 on 2018-07-11 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_studentinfo_std_grade_point_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentinfo',
            old_name='std_grade_point_total',
            new_name='std_grade_point_total_subject_avg',
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='std_grade_point_total_sum',
            field=models.FloatField(blank=True, null=True, verbose_name='Total GPA'),
        ),
    ]