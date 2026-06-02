from django.shortcuts import render, get_object_or_404,redirect
from .models import News
from .models import News, Comment
from .forms import CommentForm
from django.shortcuts import redirect

def news_list(request):
    news = News.objects.all().order_by('-created_at')

    return render(request, 'news/news_list.html', {
        'news': news
    })




def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = news.comments.all()

    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.news = news
        comment.save()
        return redirect('news_detail', pk=news.pk)

    return render(request, 'news/news_detail.html', {
        'news': news,
        'comments': comments,
        'form': form
    })
# Create your views here.
