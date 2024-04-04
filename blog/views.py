from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# Home
def home(request):
 posts = Post.objects.all()
 return render(request, 'blog/home.html', {'posts':posts})

# About
def about(request):
 return render(request, 'blog/about.html')

# Contact
def contact(request):
 return render(request, 'blog/contact.html')

# Dashboard
def dashboard(request):
 if request.user.is_authenticated:
  user = request.user
  posts = Post.objects.filter(user=user)
  full_name = user.get_full_name()
  gps = user.groups.all()
  return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps})
 else:
  return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
 logout(request)
 return HttpResponseRedirect('/')

# Sigup
def user_signup(request):
 if request.method == "POST":
  form = SignUpForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! You have become an Author.')
   user = form.save()
   group = Group.objects.get(name='Author')
   user.groups.add(group)
 else:
  form = SignUpForm()
 return render(request, 'blog/signup.html', {'form':form})

# Login
def user_login(request):
 if not request.user.is_authenticated:
  if request.method == "POST":
   form = LoginForm(request=request, data=request.POST)
   if form.is_valid():
    uname = form.cleaned_data['username']
    upass = form.cleaned_data['password']
    user = authenticate(username=uname, password=upass)
    if user is not None:
     login(request, user)
     messages.success(request, 'Logged in Successfully !!')
     return HttpResponseRedirect('/dashboard/')
  else:
   form = LoginForm()
  return render(request, 'blog/login.html', {'form':form})
 else:
  return HttpResponseRedirect('/dashboard/')

# Add New Post
@login_required
def add_post(request):
 if request.user.is_authenticated:
  if request.method == 'POST':
   form = PostForm(request.POST)
   if form.is_valid():
   
    title = form.cleaned_data['title']
    desc = form.cleaned_data['desc']
    user = request.user
    pst = Post(title=title, desc=desc,user=user)
    pst.save()
    messages.success(request, 'Congratulations!! Post added successfully.')
    form = PostForm()
  else:
   form = PostForm()
  return render(request, 'blog/addpost.html', {'form':form})
 else:
  return HttpResponseRedirect('/login/')

# Update/Edit Post
def update_post(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pi = Post.objects.get(pk=id)
      form = PostForm(request.POST, instance=pi)
      if form.is_valid():
        form.save()
        messages.success(request, 'Congratulations!! Post updated successfully.')
    else:
      pi = Post.objects.get(pk=id)
      form = PostForm(instance=pi)
    return render(request, 'blog/updatepost.html', {'form':form})
  else:
    return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pi = Post.objects.get(id=id)
      pi.delete()
      messages.success(request, 'Congratulations!! Post deleted successfully.')
      return HttpResponseRedirect('/dashboard/')
    else:
      return HttpResponseRedirect('/dashboard/')
  else:
    return HttpResponseRedirect('/login/')