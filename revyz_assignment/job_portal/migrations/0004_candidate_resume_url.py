# Generated by Django 3.2.19 on 2023-07-14 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0003_auto_20230713_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='resume_url',
            field=models.URLField(blank=True),
        ),
    ]
