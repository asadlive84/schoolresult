# Generated by Django 2.1rc1 on 2018-07-24 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_auto_20180725_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='marks',
            name='first_part_mcq',
            field=models.FloatField(blank=True, null=True, verbose_name='1st MCQ'),
        ),
        migrations.AddField(
            model_name='marks',
            name='first_part_theory',
            field=models.FloatField(blank=True, null=True, verbose_name='1st Theory'),
        ),
        migrations.AddField(
            model_name='marks',
            name='second_part_mcq',
            field=models.FloatField(blank=True, null=True, verbose_name='2nd MCQ'),
        ),
        migrations.AddField(
            model_name='marks',
            name='second_part_theory',
            field=models.FloatField(blank=True, null=True, verbose_name='2nd Theory'),
        ),
        migrations.AlterField(
            model_name='stdsubject',
            name='first_part_mcq_full_marks',
            field=models.FloatField(blank=True, null=True, verbose_name='First Part MCQ Marks'),
        ),
        migrations.AlterField(
            model_name='stdsubject',
            name='first_part_theory_full_marks',
            field=models.FloatField(blank=True, null=True, verbose_name='First Part Theory Marks'),
        ),
        migrations.AlterField(
            model_name='stdsubject',
            name='second_part_mcq_full_marks',
            field=models.FloatField(blank=True, null=True, verbose_name='Second MCQ Marks'),
        ),
        migrations.AlterField(
            model_name='stdsubject',
            name='second_part_theory_full_marks',
            field=models.FloatField(blank=True, null=True, verbose_name='First Part Theory Marks'),
        ),
    ]