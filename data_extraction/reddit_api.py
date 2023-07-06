import os
import praw
import datetime
from data_extraction.models import DailyBestPost, DBPComment, PostByTopic, PBTComment
from praw.models import MoreComments

reddit = praw.Reddit(
        client_id="uf8QZotbEf1lKqi2KznGVA",
        client_secret="dCyXHjerk6itKE7uR0gyHxQ-iNyNAA",
        user_agent="my user agent",
    )

def get_daily_best_posts():
    subreddit = reddit.subreddit('all')
    posts = []
    DailyBestPost.objects.all().delete()

    for post in subreddit.top('day', limit=3):
        data = {
            'title': post.title,
            'url': 'https://www.reddit.com' + post.permalink,
            'body': post.selftext,
            'score': post.score,
            'created_utc': datetime.datetime.fromtimestamp(post.created_utc),
        }
        posts.append(data)

    daily_best_posts = [DailyBestPost(**post) for post in posts]
    DailyBestPost.objects.bulk_create(daily_best_posts)

    comments = []
    for post in daily_best_posts:
        submission = reddit.submission(url=post.url)
        submission.comments.replace_more(limit=0)
        post_comments = submission.comments.list()
        for comment in post_comments:
            comment_data = {
                'post': post,
                'body': comment.body,
                'score': comment.score,
                'created_utc': datetime.datetime.fromtimestamp(comment.created_utc),
            }
            comments.append(comment_data)

    daily_best_posts_comments = [DBPComment(**comment) for comment in comments]
    DBPComment.objects.bulk_create(daily_best_posts_comments)

    num_posts = len(posts)
    num_comments = len(comments)

    return {'posts': posts, 'comments': comments, 'num_posts': num_posts, 'num_comments': num_comments}

def get_posts_by_topic(topic, date_range, post_number):
    subreddit = reddit.subreddit('all')
    keyword = topic.lower()

    PostByTopic.objects.filter(topic=topic).delete()
    PBTComment.objects.filter(topic=topic).delete()

    posts = [
        PostByTopic(
            title=post.title,
            url='https://www.reddit.com' + post.permalink,
            body=post.selftext,
            score=post.score,
            topic=topic,
            created_utc=datetime.datetime.fromtimestamp(post.created_utc)
        )
        for post in subreddit.search(keyword, time_filter=date_range, limit=int(post_number))
        if keyword in post.title.lower()
    ]
    PostByTopic.objects.bulk_create(posts, batch_size=1000)

    comments = [
        PBTComment(
            post_id=post.id,
            body=comment.body,
            score=comment.score,
            topic=topic,
            created_utc=datetime.datetime.fromtimestamp(comment.created_utc)
        )
        for post in PostByTopic.objects.filter(topic=topic)
        for comment in reddit.submission(url=post.url).comments.list()
        if not isinstance(comment, MoreComments)
    ]
    PBTComment.objects.bulk_create(comments, batch_size=1000)

    num_posts = len(posts)
    num_comments = len(comments)

    return {'posts': posts, 'comments': comments, 'num_posts': num_posts, 'num_comments': num_comments}