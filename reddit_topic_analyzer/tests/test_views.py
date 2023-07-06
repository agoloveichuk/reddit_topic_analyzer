from django.test import RequestFactory, TestCase
from django.shortcuts import render

from reddit_topic_analyzer.views import home, search_results

class RedditDataExtractionTestCase(TestCase):
    def setUp(self):
        # Стоврення фабрик запитів 
        self.factory = RequestFactory()

    def test_home_view(self):
        # Створення GET запиту до "home" представлення 
        request = self.factory.get('/')
        response = home(request)

        # Перевірка чи 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Перевірка чи відповідь містить очікуваний конетент 
        self.assertIn('posts', response.content.decode())
        self.assertIn('num_posts', response.content.decode())
        self.assertIn('num_comments', response.content.decode())
        self.assertIn('top_entities', response.content.decode())
        self.assertIn('word_cloud_data', response.content.decode())
        self.assertIn('plot_div', response.content.decode())
        self.assertIn('chart', response.content.decode())
        self.assertIn('top_phrases', response.content.decode())

    def test_search_results_view(self):
        # Create a GET request for the search_results view with query parameters
        request = self.factory.get('/search_results/', {'topic': 'python', 'date_range': 'week'})
        response = search_results(request)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected content
        self.assertIn('posts', response.content.decode())
        self.assertIn('num_posts', response.content.decode())
        self.assertIn('num_comments', response.content.decode())
        self.assertIn('date_range', response.content.decode())
        self.assertIn('topic', response.content.decode())
        self.assertIn('top_entities', response.content.decode())
        self.assertIn('word_cloud_data', response.content.decode())
        self.assertIn('plot_div', response.content.decode())
        self.assertIn('chart', response.content.decode())
        self.assertIn('top_phrases', response.content.decode())