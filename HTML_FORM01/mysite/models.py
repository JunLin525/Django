from django.db import models

# Create your models here.
class Mood(models.Model):
    status =models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.status
    

class Post(models.Model):
    mood =models.ForeignKey('Mood', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, default='我不想說')
    message= models.TextField(max_length=150)
    del_pass=models.CharField(max_length=50)
    pub_time=models.DateField(auto_now=True)
    enabled=models.BooleanField(default=False)

    def __str__(self):
        return self.message