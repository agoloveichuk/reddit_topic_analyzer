import base64
from io import BytesIO
from wordcloud import WordCloud
from datetime import datetime, timedelta
from django.db.models import Count
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from data_extraction.models import PostByTopic, PBTComment, DailyBestPost, DBPComment
from data_processing import spacy_utils
from django.db.models.functions import Extract, ExtractHour

def get_word_cloud_data(top_entities):
    entity_freq = {name: freq for name, freq in top_entities}
    wordcloud = WordCloud(width=2000, height=600, background_color='white').generate_from_frequencies(entity_freq)

    fig = px.imshow(wordcloud.to_array(), binary_string=True)
    fig.update_layout(width=400, height=400, margin=dict(l=0, r=0, t=0, b=0))
    img_buffer = BytesIO()
    fig.write_image(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')

    return img_str

def posts_comments_per_day_chart(date_range, topic):
    now = datetime.now()
    if date_range == 'day':
        start_date = now - timedelta(days=1)
    elif date_range == 'week':
        start_date = now - timedelta(weeks=1)
    elif date_range == 'month':
        start_date = now - timedelta(days=30)
    elif date_range == 'year':
        start_date = now - timedelta(days=365)
    else:
        start_date = None

    if start_date:
        post_counts = (
            PostByTopic.objects
            .filter(topic=topic, created_utc__gte=start_date)
            .annotate(year=Extract('created_utc', 'year'))
            .annotate(month=Extract('created_utc', 'month'))
            .annotate(day=Extract('created_utc', 'day'))
            .values('year', 'month', 'day')
            .annotate(count=Count('created_utc'))
        )
        comment_counts = (
            PBTComment.objects
            .filter(post__topic=topic, created_utc__gte=start_date)
            .annotate(year=Extract('created_utc', 'year'))
            .annotate(month=Extract('created_utc', 'month'))
            .annotate(day=Extract('created_utc', 'day'))
            .values('year', 'month', 'day')
            .annotate(count=Count('created_utc'))
        )
        post_df = pd.DataFrame(post_counts)
        comment_df = pd.DataFrame(comment_counts)
        df = post_df.merge(comment_df, on=['year', 'month', 'day'], how='outer')
        df['Date'] = pd.to_datetime(df[['year', 'month', 'day']])
        data = [
            go.Bar(
                x=df['Date'],
                y=df['count_x'],
                name='Posts'
            ),
            go.Bar(
                x=df['Date'],
                y=df['count_y'],
                name='Comments'
            )
        ]
        layout = go.Layout(
            barmode='group',
            title='Number of Posts and Comments per Day',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Count'),
        )
        fig = go.Figure(data=data, layout=layout)
        return fig
    
def posts_comments_per_day_chart_daily():
    comment_counts = (
        DBPComment.objects
        .annotate(hour=ExtractHour('created_utc'))
        .values('hour')
        .annotate(count=Count('created_utc'))
    )
    comment_df = pd.DataFrame(comment_counts)
    comment_df['Time'] = comment_df['hour'].apply(lambda x: datetime.strptime(str(x), '%H').strftime('%I %p'))
    
    data = [
        go.Bar(
            x=comment_df['Time'],
            y=comment_df['count'],
            name='Comments'
        )
    ]
    layout = go.Layout(
        barmode='group',
        title='Number of Comments per Hour',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Count'),
    )
    fig = go.Figure(data=data, layout=layout)
    return fig


def get_sentiment_over_time(data_range, topic):
    if data_range == 'all':
        posts = PostByTopic.objects.filter(title__icontains=topic)
        comments = PBTComment.objects.filter(body__icontains=topic)
    else:
        today = datetime.now()
        if data_range == 'day':
            start_date = today - timedelta(days=1)
        elif data_range == 'week':
            start_date = today - timedelta(weeks=1)
        elif data_range == 'month':
            start_date = today - timedelta(weeks=4)
        elif data_range == 'year':
            start_date = today - timedelta(weeks=5)
        
        posts = PostByTopic.objects.filter(
            created_utc=start_date, 
            topic=topic
        )
        comments = PBTComment.objects.filter(
            created_utc__gte=start_date,
            topic=topic
        )

    comment_sentiments = []
    for comment in comments:
        sentiment = spacy_utils.get_sentiment(comment.body)
        comment_sentiments.append({
            'timestamp': comment.created_utc,
            'sentiment': sentiment,
        })

    data = []
    for sentiment_data in comment_sentiments:
        data.append({
            'timestamp': sentiment_data['timestamp'],
            'sentiment': sentiment_data['sentiment'],
            'date': sentiment_data['timestamp'].strftime('%Y-%m-%d')
        })
    df = pd.DataFrame(data)

    fig = px.scatter(df, x='date', y='sentiment', title=f'Sentiment Analysis over Time for "{topic}"')
    fig.update_layout(xaxis_title='Time', yaxis_title='Sentiment Score')
    return fig

def get_sentiment_over_time_daily():
    posts = DailyBestPost.objects.all()
    comments = DBPComment.objects.all()

    comment_sentiments = []
    for comment in comments:
        sentiment = spacy_utils.get_sentiment(comment.body)
        comment_sentiments.append({
            'timestamp': comment.created_utc,
            'sentiment': sentiment,
        })

    data = []
    for sentiment_data in comment_sentiments:
        timestamp = sentiment_data['timestamp']
        # Truncate the timestamp to the nearest minute
        timestamp = timestamp.replace(second=0, microsecond=0)
        data.append({
            'timestamp': timestamp,
            'sentiment': sentiment_data['sentiment'],
            'date': timestamp.strftime('%Y-%m-%d %H:%M')  # Include minutes in the date format
        })

    # Aggregate the sentiment data at a minute level
    minute_sentiments = (
        pd.DataFrame(data)
        .groupby('date')
        .agg(sentiment_count=('sentiment', 'count'), sentiment_sum=('sentiment', 'sum'))
        .reset_index()
    )

    # Calculate the average sentiment score for each minute
    minute_sentiments['sentiment_avg'] = minute_sentiments['sentiment_sum'] / minute_sentiments['sentiment_count']

    fig = px.scatter(minute_sentiments, x='date', y='sentiment_avg', title='Sentiment Analysis over Time for daily posts')
    fig.update_layout(xaxis_title='Time', yaxis_title='Sentiment Score')

    return fig

