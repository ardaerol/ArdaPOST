from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login,authenticate,logout
from .models import Post,Comment,Like,Share
from .forms import CustomUserChangeForm,PostForm,CustomUserCreationForm
from .forms import CustomAuthenticationForm,CommentForm
from django.urls import reverse
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                messages.success(request,f'Welcome Account created for {username}!')
                return redirect(reverse('posts:post_list'))
    else:
        form = CustomUserCreationForm()
            
    return render(request,'posts/register.html',context={'form':form})
        

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)
            username = user.username
            messages.success(request,f'Welcome {username}!')
            return redirect(reverse('posts:post_list'))
        else:
            messages.error(request,"Invalid username or password")
    else:
        form = CustomAuthenticationForm()
        
    return render(request,'posts/login.html',context={'form':form})
    

@login_required
def logout_view(request):
    logout(request)
    messages.info(request,"You have been logged out")
    return redirect(reverse('posts:post_list'))

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('posts:post_list'))
    else:
        form = PostForm()
    return render(request,'posts/create_post.html',context={'form':form})


@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request,'posts/post_list.html',{'posts':posts})

@login_required
def edit_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('posts:post_list'))
    else:
        form = PostForm(instance=post)
    return render(request,'posts/edit_post.html',{'form':form})

@login_required
def delete_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        if request.user == post.author:
            post.delete()
            return redirect(reverse('posts:post_list'))
    return render(request,'posts/confirm_delete.html',{'post':post})


@login_required
def add_comment(request,post_id,parent_id=None):
    post = get_object_or_404(Post,id=post_id)
    parent_comment = get_object_or_404(Comment,id=parent_id) if parent_id else None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent = parent_comment
            comment.save()
            return redirect(reverse('posts:post_list'))
    else:
        form = CommentForm()
    return render(request,'posts/add_comment.html',{'form':form,'post':post})


@login_required
def edit_comment(request,comment_id):
    comment = get_object_or_404(Comment,id=comment_id)
    if request.user != comment.author:
        return redirect(reverse('posts:post_list'))
    if request.method ==  'POST':
        form = CommentForm(request.POST,instance=comment)
        if form.is_valid():
            form.save()
            return redirect(reverse('posts:post_list'))
    else:
        form = CommentForm(instance=comment)
    return render(request,'posts/edit_comment.html',context={'form':form})


@login_required
def delete_comment(request,comment_id):
    comment = get_object_or_404(Comment,id=comment_id)
    
    comment.delete()
    return redirect(reverse('posts:post_list'))


@login_required
def like_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    like,created = Like.objects.get_or_create(user=request.user,post=post)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def share_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    share,created=Share.objects.get_or_create(user=request.user,post=post)
    if not created:
        share.delete()
    return redirect(request.META.get('HTTP_REFERER') or 'post_list')


@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Your profile was successfully updated!')
            return redirect(reverse('posts:profile'))
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request,'posts/profile.html',context={'form':form,'user':request.user})