from django.shortcuts import render
from .models import News, NewsCategory, Comment, Banner
from django.conf import settings
from utils import restful
from .serializers import NewsSerializer, CommentSerializer
from django.http import Http404
from .forms import PublicCommentForm
from apps.xfzauth.decorators import xfz_login_required
from django.db.models import Q


# Create your views here.


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('author', 'category').all()[0:count]
    categories = NewsCategory.objects.all()
    banners = Banner.objects.all()
    return render(request, 'news/index.html', locals())


def news_list(request):
    #通过p参数来制定要获取第几页的数据， 并且p参数通过查询字符串的方式传过来
    page = int(request.GET.get('p', 1))
    category_id = int(request.GET.get('category_id', 0))   #如果分类为0，不进行分类查找，直接全部按时间倒序排序

    start = (page-1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        newses = News.objects.select_related('author', 'category').all()[start:end]   #.values('') 得不到news的category分类信息和author作者信息
    else:
        newses = News.objects.select_related('author', 'category').filter(category__id=category_id)[start:end]

    serializer = NewsSerializer(newses, many=True)
    return restful.result(data=serializer.data)


def news_detail(request, news_id):
    try:
        news = News.objects.select_related('author', 'category').prefetch_related('comments__author').get(pk=news_id)
        return render(request, 'news/news_detail.html', locals())
    except News.DoesNotExist:
        raise Http404


@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        content = form.cleaned_data.get('content')
        comment = Comment.objects.create(content=content, news=news, author=request.user)
        serializer = CommentSerializer(comment)
        return restful.result(data=serializer.data)
    else:
        return restful.params_error(message=form.get_errors())


def search(request):
    q = request.GET.get('q')
    if q:
        newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
    return render(request, 'search/search.html', locals())