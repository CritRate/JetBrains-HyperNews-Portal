from typing import List
import itertools
from datetime import datetime

from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.shortcuts import redirect
import json
import random


# Create your views here.

def home_view(request):
    return redirect('news:news')


def news_by_id(request, id):
    with open(f'{settings.NEWS_JSON_PATH}', 'r') as file:
        for post in json.load(file):
            if post['link'] == id:
                return render(request, 'news_id.html',
                              context={'title': post['title'],
                                       'created': post['created'],
                                       'text': post['text']})
    return HttpResponse('Wrong news id!')


def news(request):
    with open(f'{settings.NEWS_JSON_PATH}', 'r') as file:
        posts: List = json.load(file)
        posts.sort(key=lambda post: post.get('created'), reverse=True)
        if q := request.GET.get('q'):
            posts[:] = [x for x in posts if q in x.get('title')]
        posts = [{'date': date, 'news': list(_news)} for date, _news in
                 itertools.groupby(posts, lambda x: datetime.strptime(x.get('created'), "%Y-%m-%d %H:%M:%S").strftime(
                     "%Y-%m-%d"))]

    return render(request, 'news.html', context={'posts': posts})


def create_post(request):
    if request.method == 'POST':
        with open(f'{settings.NEWS_JSON_PATH}', 'r+') as file:
            data = json.load(file)
            data.append({
                'created': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                'text': request.POST['text'],
                'title': request.POST['title'],
                'link': random.randrange(100000, 999999)
            })
            file.seek(0)
            file.truncate()
            json.dump(data, file)
        return redirect('news:news')
    return render(request, 'create_post.html')
