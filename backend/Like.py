from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post, Like

@require_http_methods(["GET", "POST"])
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        user = request.user  # get the current user
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
    likes_count = post.count_likes()  # get the updated number of likes for the post
    return JsonResponse({'likes': likes_count, 'liked': liked})