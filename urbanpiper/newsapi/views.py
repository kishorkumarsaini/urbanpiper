import requests
from django.shortcuts import render
from django.conf import settings
from pymongo import MongoClient
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from aylienapiclient import textapi
from hackernews import HackerNews

# Create your views here.
DB_CLINET = MongoClient('localhost', 27017)
DB = DB_CLINET['articles']


class TopArticalView(APIView):
    def get(self,request):
        saved_items = DB.saved_items
        hacker_news = HackerNews()
        response = []
        for item_id in hacker_news.top_stories()[:5]:
            article = vars(hacker_news.item(item_id))
            response.append(article)
        results = saved_items.insert_many(response)
        for r in response:
            r.pop('_id')
        return Response(response, status=status.HTTP_200_OK)


class SentiMentView(APIView):

    def get(self,request):
        #import pdb; pdb.set_trace()
        app_id, client_id = settings.AYLIEN.values()
        client = textapi.Client(app_id, client_id)
        sentiment = []
        articles = DB.saved_items.find()
        for article in articles:
            sentiment.append(
                client.Sentiment({'text': article.get('title')})
            )
        return Response(sentiment)


class ArticleInfoView(APIView):
    def get(self,request):
        response = []
        articles = DB.saved_items.find()
        for article in articles:
            article.pop('_id')
            for item in ['kids','descendants','time','type']:
                article.pop(item)
            response.append(article)
        return Response(response)


class SearchArticleView(APIView):
    def get(self,request):
        #import pdb; pdb.set_trace()
        response = []
        articles = DB.saved_items.find()
        for article in articles:
            article.pop('_id')
            response.append({'text':article.get('title')})

        
        db = DB_CLINET['some_collection']
        collection = db.collection

        collection.insert(response[0])
        collection.create_index([('title', 'text')])

        search_this_string ="regular expression to detect a"
        result=collection.find({"$text": {"$search": search_this_string}}).count()

        return Response(result)