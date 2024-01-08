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
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskAssignment(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tasks_users')
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks_users')
