import json
import os
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import plotly
import praw

from data_extraction import reddit_api
from data_processing import spacy_utils
from data_visualisation import pyplot_utils

import plotly.graph_objs as go
import time

reddit = praw.Reddit(
    client_id="uf8QZotbEf1lKqi2KznGVA",
    client_secret="dCyXHjerk6itKE7uR0gyHxQ-iNyNAA",
    user_agent="my user agent",
)

def home(request):
    result = {}
    topic = ''
    date_range = "None"

    start_time = time.time()
    result = reddit_api.get_daily_best_posts()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} get_daily_best_posts seconds")

    start_time = time.time()
    top_entities = spacy_utils.get_top_daily_entities()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} get_top_daily_entities seconds")
    word_cloud_data = pyplot_utils.get_word_cloud_data(top_entities)
    chart_data = pyplot_utils.posts_comments_per_day_chart_daily()
    plot_div = chart_data.to_html(full_html=False)
    chart_data_sent = pyplot_utils.get_sentiment_over_time_daily()
    chart = chart_data_sent.to_html(full_html=False)
    top_phrases = spacy_utils.get_top_phrases(topic)

    
    print(f"Execution time: {end_time - start_time} all methods done seconds")
    
    context = {
        'posts': result["posts"],
        'num_posts': result["num_posts"],
        'num_comments': result["num_comments"],
        'top_entities': top_entities,
        'word_cloud_data': word_cloud_data,
        'plot_div': plot_div,
        'chart': chart,
        'top_phrases': top_phrases,
    }

    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

def search_results(request):
    topic = request.GET.get('topic')
    date_range = request.GET.get('date_range')
    post_number = request.GET.get('post_number')

    result = reddit_api.get_posts_by_topic(topic, date_range, post_number)
    top_entities = spacy_utils.get_top_entities(topic)
    chart_data = pyplot_utils.posts_comments_per_day_chart(date_range, topic)
    plot_div = chart_data.to_html(full_html=False)
    chart_data_sent = pyplot_utils.get_sentiment_over_time(date_range, topic)
    chart = chart_data_sent.to_html(full_html=False)
    sentiment_results = spacy_utils.analyze_sentiment_scores(date_range, topic)
    sentiment_results_posts = spacy_utils.analyze_sentiment_scores_posts(date_range, topic)
    
    context = {
        'posts': result["posts"],
        'num_posts': result["num_posts"],
        'num_comments': result["num_comments"],
        'date_range': date_range,
        'topic': topic,
        'top_entities': top_entities,
        'plot_div': plot_div,
        'chart': chart,
        'sentiment_results': sentiment_results,
        'sentiment_results_posts': sentiment_results_posts,
    }
    return render(request, 'search_results.html', context)

def about(request):
    return render(request, 'about.html')