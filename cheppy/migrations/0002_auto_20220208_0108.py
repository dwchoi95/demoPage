# Generated by Django 3.2.9 on 2022-02-08 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheppy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='deadline',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='grade',
            name='result',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='grade',
            name='state',
            field=models.CharField(max_length=10),
        ),
    ]
