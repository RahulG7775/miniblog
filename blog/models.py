from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
 id = models.AutoField(primary_key=True)
 title = models.CharField(max_length=150)
 desc = models.TextField()
 user = models.ForeignKey(User, on_delete=models.CASCADE,)
 