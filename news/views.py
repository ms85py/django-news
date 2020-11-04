from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, Http404

import json
import itertools
import datetime

from django.conf import settings
from django.shortcuts import redirect


class ComingSoon(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsMain(View):
    def get(self, request, *args, **kwargs):
        # check if there's a search going on
        query = request.GET.get('q')
        if query:
            with open("news.json", "r") as json_file:
                data = json.load(json_file)
                to_show = []
                for ea in data:
                    if query in ea['title']:
                        to_show.append(ea)
                sorted_data = sorted(to_show, key=lambda x: x['created'], reverse=True)
                grouped = itertools.groupby(sorted_data, lambda y: y['created'][:10])
                final = [{'date': date, 'values': list(values)} for date, values in grouped]
                context = {'ctx': final}
                return render(request, "news/main.html", context=context)

        # show news if no query was found
        with open("news.json", "r") as json_file:
            data = json.load(json_file)
            # sort data by created
            sorted_data = sorted(data, key=lambda x: x['created'], reverse=True)
            # group data by Y-m-d of creation!
            # important so news made on the same day are listed with only one date
            grouped = itertools.groupby(sorted_data, lambda y: y['created'][:10])
            # making it a new dict with date as date and values as a list of values of each news
            final = [{'date': date, 'values': list(values)} for date, values in grouped]
            context = {'ctx': final}
            return render(request, "news/main.html", context=context)


class NewsView(View):
    def get(self, request, news_id, *args, **kwargs):
        # opening json, checking if news_id is valid
        # if not -> 404; if it is -> display appropriate news
        with open(settings.NEWS_JSON_PATH, "r") as json_file:
            news = json.load(json_file)
            if news_id > len(news) + 1:
                raise Http404
            data = news[news_id - 1]
            context = {"ctx": data}
        return render(request, "news/index.html", context=context)


class CreateNews(View):
    def get(self, request, *arg, **kwargs):
        # simple render return to display the create page
        return render(request, "news/create.html")

    def post(self, request, *args, **kwargs):
        # getting title/text/making a date
        title = request.POST.get('title')
        text = request.POST.get('text')
        date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # opening file with read permissions to get new link integer
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news_file = json.load(json_file)
            link = len(news_file) + 1

        # opening with write permissions, updating with the new news and dumping it
        # then redirect back to the /news/ page
        with open(settings.NEWS_JSON_PATH, 'w') as write_json:
            to_add = {
                "created": date, "text": str(text), "title": str(title), "link": link
            }
            news_file.append(to_add)
            json.dump(news_file, write_json)

        return redirect('/news/')

