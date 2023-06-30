from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    following_count = models.IntegerField(blank=True)
    followers_count = models.IntegerField(blank=True)

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField()
    likes = models.IntegerField()

    def __str__(self):
        return f'post by {self.username}, on {self.date}: "{self.post}"'
    

class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers")
    follows = models.ManyToManyField(User,related_name="following")

    def __str__(self):
        return f'{self.user}'
    
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="liker")
    post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="liked")

    def __str__(self):
        return f'{self.user} likes {self.post}'