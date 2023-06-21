from django.db import models
from django.contrib.auth.models import User
# Create your models here.
RANKS = (('جندي', 'جندي'), ('عريف', 'عريف'), ('رقيب', 'رقيب'), ('رقيب اول', 'رقيب اول'), ('مساعد', 'مساعد'), ('مساعد اول', 'مساعد اول'),
         ('ملازم', 'ملازم'), ('ملازم اول', 'ملازم اول'), ('نقيب', 'نقيب'), ('رائد', 'رائد'), ('مقدم', 'مقدم'), ('عقيد', 'عقيد'), ('عميد', 'عميد'))
class Officer(models.Model):
    class UserTypes(models.TextChoices):
        HigherOfficer = '1','رئيس الفرع'
        Officer = '2','ضابط'
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    officer_name = models.CharField(max_length=256,verbose_name="اسم الضابط")
    rank = models.CharField(
        max_length=64, choices=RANKS, blank=True, null=True)
    role = models.CharField(max_length=50,choices=UserTypes.choices)
    def __str__(self):
        return self.user.username


class PersonalNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username