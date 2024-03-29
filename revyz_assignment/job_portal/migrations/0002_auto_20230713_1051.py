# Generated by Django 3.2.19 on 2023-07-13 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='candidate',
            name='resume_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='location',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='tech_skills',
        ),
        migrations.AddField(
            model_name='candidate',
            name='tech_skills',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.DeleteModel(
            name='TechSkill',
        ),
    ]
