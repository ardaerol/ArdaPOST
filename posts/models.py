from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,Group,Permission
from PIL import Image

# Create your models here.

class CustomUser(AbstractUser): # kullanıcılarımız için oluşturduğumuz özel model ve profilin alması gereken özellikler
    bio = models.TextField(max_length=200,blank=True)
    location = models.CharField(max_length=50,blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    groups = models.ManyToManyField(Group,related_name='custom_user_set',blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name='custom_user_set',blank=True)

    def __str__(self):
        return self.username



class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts') #hangi kullanıcı ve kullanıcı silindi,ğinde postlara ne olkacağı
    content = models.TextField()
    image = models.ImageField(upload_to='posts/',blank=True,null=True) # post un fotoları posts/ altına yüklenecek
    created_at = models.DateTimeField(auto_now_add=True) #otomatik oluşturulma tarihi
    updated_ad = models.DateTimeField(auto_now=True) #otomatik güncellenme tarihi


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            img = img.resize((800,500),Image.LANCZOS)
            img.save(self.image.path)
    
    def __str__(self):
        return f"{self.auther.username} - {self.created_at.strftime('%Y-%m-%d %H:%m')}"
    
    def total_likes(self):
        return self.likes.count()
    
    def total_shares(self):
        return self.shares.count()
    def total_comments(self):
        return self.comments.count()
    

class Like(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post}"
    

class Share(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='shares')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} shared {self.post}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True,blank=True,related_name='replies') #kendisi yorum atarsa

    def __str__(self):
        return f"{self.author.username} comment {self.created_at.strftime("%Y-%m-%d %H:%M")}"
    
    def get_replies(self):
        return self.replies.all()
    