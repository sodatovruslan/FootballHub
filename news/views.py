from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Comment, CommentLike
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

def news_list(request):
    news = News.objects.all().order_by('-created_at')

    return render(request, 'news/news_list.html', {
        'news': news
    })


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = news.comments.filter(parent_comment=None).prefetch_related('replies__user', 'likes')

    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if not request.user.is_authenticated:
            return redirect('login')

        comment = form.save(commit=False)
        comment.user = request.user
        comment.news = news

        parent_comment_id = request.POST.get('parent_comment_id')
        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
            comment.parent_comment = parent_comment

        comment.save()
        return redirect('news_detail', pk=news.pk)

    return render(request, 'news/news_detail.html', {
        'news': news,
        'comments': comments,
        'form': form
    })


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    like, created = CommentLike.objects.get_or_create(
        comment=comment,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect('news_detail', pk=comment.news.pk)
