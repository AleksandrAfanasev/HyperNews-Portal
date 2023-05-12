from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import json
from datetime import datetime

# Create your views here.

class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news")


class NewsView(View):
    def get(self, request, link):
        with open(settings.NEWS_JSON_PATH) as json_file:
            articles = json.load(json_file)
        for article in articles:
            if article["link"] == link:
                return render(request, 'news/news.html', {'article': article})

class NewsListView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')

        with open(settings.NEWS_JSON_PATH, encoding="utf-8") as f:
            json_file = json.load(f)
        articles = sorted(json_file, key=lambda x: x["created"], reverse=True)
        for article in articles:
            article["created"] = article["created"][:10]

        if q:
            articles = [article for article in articles if q in article['title']]
            articles = sorted(articles, key=lambda data: data['created'], reverse=True)

        return render(request, 'news/news_list.html', context={"data": articles})




class CreateNews(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create_news.html', context={})

    def post(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, encoding="utf-8") as f:
            json_file = json.load(f)
        news_id = 1
        news = set([n["link"] for n in json_file])
        while news_id in news:
            news_id += 1
        news_create = {
            "created": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "text": request.POST["text"],
            "title": request.POST["title"],
            "link": news_id
        }
        json_file.append(news_create)
        with open(settings.NEWS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(json_file, f)
        return redirect("/news")