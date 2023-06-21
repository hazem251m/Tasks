import datetime
from django.db import models
from accounts.models import Officer
# Create your models here.

class Task(models.Model):
    class State(models.TextChoices):
        IN_PROGRESS = 'جاري التنفيذ','جاري التنفيذ'
        PENDING = 'بإنتظار تأكيد الإنهاء','بإنتظار تأكيد الإنهاء'
        COMPLETED = 'تم إنجازه','تم إنجازه'

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    task_attachment = models.FileField(upload_to='task_attachments/', blank=True, null=True)
    state = models.CharField(max_length=32, choices=State.choices, default=State.IN_PROGRESS)
    created = models.DateTimeField(auto_now_add=True)
    officers = models.ManyToManyField(Officer, related_name='tasks')

    def __str__(self):
        return self.title

class TaskNotes(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notes')
    officer = models.ForeignKey(Officer,on_delete=models.CASCADE,related_name="task_notes")
    note = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task.title
