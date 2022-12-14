# Generated by Django 3.2.3 on 2021-05-23 20:02

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=20)),
                ('title', models.CharField(max_length=20)),
                ('body', ckeditor.fields.RichTextField()),
                ('message_slug', models.SlugField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentname', models.CharField(max_length=20)),
                ('week', models.CharField(max_length=10)),
                ('answerscore', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('std_name', models.CharField(max_length=10)),
                ('std_gender', models.CharField(max_length=10)),
                ('std_age', models.IntegerField()),
                ('std_id', models.CharField(max_length=10)),
                ('std_class', models.CharField(max_length=20)),
                ('std_college', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whichweek', models.CharField(max_length=20)),
                ('week_slug', models.SlugField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('studentname', models.CharField(max_length=20)),
                ('answer', ckeditor.fields.RichTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('week', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='student.week')),
            ],
        ),
    ]
