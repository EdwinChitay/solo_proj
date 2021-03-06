from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/') 
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hashed_pw)
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
        email=request.POST['email'], password=hashed_pw)
        request.session['user_id'] = new_user.id
        return redirect('/home')
    return redirect('/') 

def login(request):
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/home')
    messages.error(request, "Email and/or password are incorrect")
    return redirect('/')

def logout(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    request.session.clear()
    return redirect('/')

def home(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_posts': Post.objects.all(),
    }
    return render(request, 'home.html', context)

def create(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if request.method == "POST":
        errors = Post.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/home')
        else:
            Post.objects.create(
            text = request.POST['text'],
            user = User.objects.get(id=request.session['user_id']),
            )
    return redirect('/home')

def delete(request, post_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if request.method == "POST":
        post_to_delete = Post.objects.get(id=post_id)
        post_to_delete.delete()
    return redirect('/home')

def like(request, post_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if request.method == "POST":
        liked_post = Post.objects.get(id=post_id)
        user_liking = User.objects.get(id=request.session['user_id'])
        liked_post.user_likes.add(user_liking)
        return redirect('/home')

def add_comment(request, post_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if request.method == "POST":
        errors = Comment.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/home')
        else:
            user = User.objects.get(id=request.session['user_id'])
            post = Post.objects.get(id=post_id)
            Comment.objects.create(comment=request.POST['comment'], user=user, post=post)
        return redirect('/home')

def profile(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'user': User.objects.get(id=user_id),
    }
    return render(request, 'profile.html', context)

def post(request, post_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    one_post = Post.objects.get(id=post_id)    
    context = {
        'post': one_post,
    }
    return render(request, 'post.html', context)

