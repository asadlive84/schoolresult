# Generated by Django 2.1b1 on 2018-07-14 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_auto_20180714_0618'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectTecher',
            fields=[
                ('stdcommon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='results.StdCommon')),
                ('teacher_name', models.CharField(max_length=100, verbose_name='Teacher Name')),
                ('teach_phone_number', models.IntegerField(verbose_name='Mobile Number')),
            ],
            bases=('results.stdcommon',),
        ),
        migrations.AddField(
            model_name='stdsubject',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='results.SubjectTecher'),
            preserve_default=False,
        ),
    ]