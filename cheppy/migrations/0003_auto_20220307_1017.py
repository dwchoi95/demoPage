# Generated by Django 2.2.12 on 2022-03-07 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheppy', '0002_assignment_timeout'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='specification',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='solution',
            name='standardization',
            field=models.TextField(blank=True, null=True),
        ),
    ]
