from django.db import models
import re 

# Create your models here.
class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(reqPOST['first_name']) <2 or len(reqPOST['last_name']) <2:
            errors['name'] = "Name must be at least 2 characters"
        if not email_checker.match(reqPOST['email']):
            errors['email'] = "Email must be valid"
        if len(reqPOST['password']) < 8:
            errors['password'] = "Password must be at least 8 chcaracters"
        if reqPOST['password'] != reqPOST['confpassword']:
            errors['password'] = "Passwords do not match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class PostManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['text']) <5:
            errors['text'] = "Post must be at least 5 characters long."
        return errors

class Post(models.Model):
    text = models.CharField(max_length=250)
    user =  models.ForeignKey(User, related_name="post_user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    objects = PostManager()

class CommentManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['comment']) == 0:
            errors['comment'] = "Comment can not be blank."
        return errors

class Comment(models.Model):
    comment = models.CharField(max_length=250)
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects =  CommentManager()