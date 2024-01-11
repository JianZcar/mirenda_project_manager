from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    members = models.ManyToManyField(CustomUser, related_name='projects')


class Task(models.Model):
    name = models.CharField(max_length=200)
    task_id = models.AutoField(primary_key=True)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True, blank=True)  # make deadline optional
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ManyToManyField(CustomUser, related_name='tasks')
