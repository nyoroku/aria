from django.shortcuts import render, get_object_or_404
from models import Latest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    news = Latest.objects.order_by('-created')[:3]
    paginator = Paginator(news, 3)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'home/index.html', {'news': news, 'page': page})


def latest_detail(request, year, month, day, new):
    new = get_object_or_404(Latest, slug=new)
    return render(request, 'home/news.html', {'new': new})


def allnews(request):
    news = Latest.objects.order_by('-created')
    paginator = Paginator(news, 6)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'home/allnews.html', {'news': news, 'page': page})









