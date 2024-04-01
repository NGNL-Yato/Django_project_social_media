from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post, Group

# Create
def create_post(request, group_id=None):
    print(f"Group ID: {group_id}")  # Debug line
    group = Group.objects.get(id=group_id) if group_id else None
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.group = group
            post.save()
            
            user_profile = user_profile.objects.get_or_create(user=request.user)
            user_profile.posts.add(post)
            
            
            if group:
                return redirect('group_posts', group_name=group.group_name)
            else:
                return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# Read
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

# Update
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'update_post.html', {'form': form})

# Delete
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return render(request, 'confirm_delete.html', {'post': post})
