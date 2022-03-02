# Generated by Django 3.2.9 on 2022-02-07 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('birth', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_no', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('problem', models.TextField()),
                ('constraint', models.TextField()),
                ('format', models.TextField()),
                ('deadline', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testsuite',
            fields=[
                ('testcase_no', models.AutoField(primary_key=True, serialize=False)),
                ('tc_no', models.IntegerField()),
                ('in_tc', models.TextField()),
                ('out_tc', models.TextField()),
                ('open_tc', models.BooleanField()),
                ('assignment_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheppy.assignment')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('submit_no', models.AutoField(primary_key=True, serialize=False)),
                ('program', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assignment_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheppy.assignment')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheppy.account')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('grade_no', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField()),
                ('score', models.IntegerField()),
                ('passfail', models.TextField()),
                ('hints', models.TextField()),
                ('feedback', models.TextField()),
                ('patch', models.TextField()),
                ('result', models.BooleanField()),
                ('submit_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheppy.submission')),
            ],
        ),
    ]
