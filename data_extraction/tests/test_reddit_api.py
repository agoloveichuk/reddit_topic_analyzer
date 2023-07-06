import praw
from django.test import TestCase
from data_extraction.models import DailyBestPost, DBPComment, PostByTopic, PBTComment 
from data_extraction import reddit_api

class RedditDataExtractionTestCase(TestCase):
    def setUp(self):
        # Set up the Reddit instance with your credentials
        self.reddit = praw.Reddit(
            client_id="uf8QZotbEf1lKqi2KznGVA",
            client_secret="dCyXHjerk6itKE7uR0gyHxQ-iNyNAA",
            user_agent="my user agent",
        )

    def test_get_daily_best_posts(self):
        # Call the function
        result = reddit_api.get_daily_best_posts()

        # Check if the function returns the expected keys in the result dictionary
        self.assertIn('posts', result)
        self.assertIn('comments', result)
        self.assertIn('num_posts', result)
        self.assertIn('num_comments', result)

        # Check if the number of posts and comments are greater than 0
        self.assertGreater(result['num_posts'], 0)
        self.assertGreater(result['num_comments'], 0)

        # Check if the DailyBestPost and DBPComment objects are created in the database
        self.assertGreater(DailyBestPost.objects.count(), 0)
        self.assertGreater(DBPComment.objects.count(), 0)

    def test_get_posts_by_topic(self):
        # Call the function with a specific topic and data range
        result = reddit_api.get_posts_by_topic('python', 'week')

        # Check if the function returns the expected keys in the result dictionary
        self.assertIn('posts', result)
        self.assertIn('comments', result)
        self.assertIn('num_posts', result)
        self.assertIn('num_comments', result)

        # Check if the number of posts and comments are greater than 0
        self.assertGreater(result['num_posts'], 0)
        self.assertGreater(result['num_comments'], 0)

        # Check if the PostByTopic and PBTComment objects are created in the database
        self.assertGreater(PostByTopic.objects.count(), 0)
        self.assertGreater(PBTComment.objects.count(), 0)
