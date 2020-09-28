# Generated by Django 3.0.5 on 2020-09-26 23:18

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RedditUser',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('submissions_karma', models.PositiveIntegerField(default=0)),
                ('comments_karma', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField()),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubReddit',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=5000)),
                ('short_description', models.CharField(max_length=500)),
                ('num_subscribers', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField()),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('body', models.CharField(blank=True, max_length=40000, null=True)),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
                ('score', models.PositiveIntegerField(default=0)),
                ('num_comments', models.PositiveIntegerField(default=0)),
                ('num_writers', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField()),
                ('retrieved_on', models.DateTimeField()),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='submission.RedditUser')),
                ('subreddit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='submission.SubReddit')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('body', models.CharField(blank=True, max_length=40000, null=True)),
                ('score', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField()),
                ('retrive_on', models.DateTimeField()),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='submission.RedditUser')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='submission.Comment')),
                ('submission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='submission.Submission')),
            ],
        ),
    ]
