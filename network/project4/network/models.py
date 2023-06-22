from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField()
    likes = models.IntegerField()
    likers = models.ManyToManyField(User,blank=True,related_name="liked")

    def __str__(self):
        return f'post by {self.username}, on {self.date}: "{self.post}"'
    

    