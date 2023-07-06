from django.db import IntegrityError
from django.utils import timezone
from django.test import TransactionTestCase
from data_extraction.models import DailyBestPost, DBPComment, PostByTopic, PBTComment

class DailyBestPostTestCase(TransactionTestCase):
    def setUp(self):
        self.post = DailyBestPost.objects.create(
            title='Test Post',
            body='Lorem ipsum dolor sit amet.',
            score=10,
            url='https://example.com',
            created_utc=timezone.now()
        )

    def test_post_title(self):
        self.assertEqual(self.post.title, 'Test Post')

    def test_post_body(self):
        self.assertEqual(self.post.body, 'Lorem ipsum dolor sit amet.')

    def test_post_score(self):
        self.assertEqual(self.post.score, 10)

    def test_post_url(self):
        self.assertEqual(self.post.url, 'https://example.com')

    def test_post_created_utc(self):
        self.assertIsNotNone(self.post.created_utc)

    def test_post_validation(self):
        with self.assertRaises(IntegrityError):
            # Перевірка відсутності обов'яхкових полів даних
            DailyBestPost.objects.create()

        with self.assertRaises(ValueError):
            # Тестування введення не коректного значення score 
            DailyBestPost.objects.create(title='Test', body='Lorem ipsum', score='score', url='https://example.com')

    def test_post_crud_operations(self):
        # CREATE
        post = DailyBestPost.objects.create(title='Test', body='Lorem ipsum', score=10, url='https://example.com')
        self.assertIsNotNone(post.id)

        # READ
        retrieved_post = DailyBestPost.objects.get(id=post.id)
        self.assertEqual(retrieved_post.title, 'Test')

        # UPDATE
        retrieved_post.title = 'Updated Test'
        retrieved_post.save()

        updated_post = DailyBestPost.objects.get(id=post.id)
        self.assertEqual(updated_post.title, 'Updated Test')

        # DELETE
        updated_post.delete()

        with self.assertRaises(DailyBestPost.DoesNotExist):
            DailyBestPost.objects.get(id=post.id)

class DBPCommentTestCase(TransactionTestCase):
    def setUp(self):
        self.post = DailyBestPost.objects.create(
            title='Test Post',
            body='Lorem ipsum dolor sit amet.',
            score=10,
            url='https://example.com',
            created_utc=timezone.now()
        )
        self.comment = DBPComment.objects.create(
            post=self.post,
            body='Test comment',
            score=5,
            created_utc=timezone.now()
        )

    def test_comment_post(self):
        self.assertEqual(self.comment.post, self.post)

    def test_comment_body(self):
        self.assertEqual(self.comment.body, 'Test comment')

    def test_comment_score(self):
        self.assertEqual(self.comment.score, 5)

    def test_comment_created_utc(self):
        self.assertIsNotNone(self.comment.created_utc)

    def test_comment_validation(self):
        with self.assertRaises(IntegrityError):
            # Test missing required fields
            DBPComment.objects.create()

        with self.assertRaises(ValueError):
            # Test invalid score value
            DBPComment.objects.create(post=self.post, body='Test comment', score='score')

        # Test valid comment creation
        comment = DBPComment.objects.create(post=self.post, body='Test comment', score=5)
        self.assertIsNotNone(comment.id)

    def test_comment_crud_operations(self):
        # Create
        comment = DBPComment.objects.create(post=self.post, body='Test comment', score=5)
        self.assertIsNotNone(comment.id)

        # Read
        retrieved_comment = DBPComment.objects.get(id=comment.id)
        self.assertEqual(retrieved_comment.body, 'Test comment')

        # Update
        retrieved_comment.body = 'Updated comment'
        retrieved_comment.save()

        updated_comment = DBPComment.objects.get(id=comment.id)
        self.assertEqual(updated_comment.body, 'Updated comment')

        # Delete
        updated_comment.delete()

        with self.assertRaises(DBPComment.DoesNotExist):
            DBPComment.objects.get(id=comment.id)

class PostByTopicTestCase(TransactionTestCase):
    def setUp(self):
        self.post = PostByTopic.objects.create(
            title='Test Post',
            body='Lorem ipsum dolor sit amet.',
            topic='Test Topic',
            score=10,
            url='https://example.com',
            created_utc=timezone.now()
        )

    def test_post_title(self):
        self.assertEqual(self.post.title, 'Test Post')

    def test_post_body(self):
        self.assertEqual(self.post.body, 'Lorem ipsum dolor sit amet.')

    def test_post_topic(self):
        self.assertEqual(self.post.topic, 'Test Topic')

    def test_post_score(self):
        self.assertEqual(self.post.score, 10)

    def test_post_url(self):
        self.assertEqual(self.post.url, 'https://example.com')

    def test_post_created_utc(self):
        self.assertIsNotNone(self.post.created_utc)

    def test_post_validation(self):
        with self.assertRaises(IntegrityError):
            # Test missing required fields
            PostByTopic.objects.create()

        with self.assertRaises(ValueError):
            # Test invalid score value
            PostByTopic.objects.create(title='Test', body='Lorem ipsum', topic='Test Topic', score='score', url='https://example.com')

        # Test valid post creation
        post = PostByTopic.objects.create(title='Test', body='Lorem ipsum', topic='Test Topic', score=10, url='https://example.com')
        self.assertIsNotNone(post.id)

    def test_post_crud_operations(self):
        # Create
        post = PostByTopic.objects.create(title='Test', body='Lorem ipsum', topic='Test Topic', score=10, url='https://example.com')
        self.assertIsNotNone(post.id)

        # Read
        retrieved_post = PostByTopic.objects.get(id=post.id)
        self.assertEqual(retrieved_post.title, 'Test')

        # Update
        retrieved_post.title = 'Updated Test'
        retrieved_post.save()

        updated_post = PostByTopic.objects.get(id=post.id)
        self.assertEqual(updated_post.title, 'Updated Test')

        # Delete
        updated_post.delete()

        with self.assertRaises(PostByTopic.DoesNotExist):
            PostByTopic.objects.get(id=post.id)

class PBTCommentTestCase(TransactionTestCase):
    def setUp(self):
        self.post = PostByTopic.objects.create(
            title='Test Post',
            body='Lorem ipsum dolor sit amet.',
            topic='Test Topic',
            score=10,
            url='https://example.com',
            created_utc=timezone.now()
        )

        self.comment = PBTComment.objects.create(
            post=self.post,
            body='Test Comment',
            topic='Test Topic',
            score=5,
            created_utc=timezone.now()
        )

    def test_comment_post(self):
        self.assertEqual(self.comment.post, self.post)

    def test_comment_body(self):
        self.assertEqual(self.comment.body, 'Test Comment')

    def test_comment_topic(self):
        self.assertEqual(self.comment.topic, 'Test Topic')

    def test_comment_score(self):
        self.assertEqual(self.comment.score, 5)

    def test_comment_created_utc(self):
        self.assertIsNotNone(self.comment.created_utc)

    def test_comment_validation(self):
        with self.assertRaises(IntegrityError):
            # Test missing required fields
            PBTComment.objects.create()

        with self.assertRaises(ValueError):
            # Test invalid score value
            PBTComment.objects.create(post=self.post, body='Test', topic='Test Topic', score='score')

        # Test valid comment creation
        comment = PBTComment.objects.create(post=self.post, body='Test', topic='Test Topic', score=8)
        self.assertIsNotNone(comment.id)

    def test_comment_crud_operations(self):
        # Create
        comment = PBTComment.objects.create(post=self.post, body='Test', topic='Test Topic', score=8)
        self.assertIsNotNone(comment.id)

        # Read
        retrieved_comment = PBTComment.objects.get(id=comment.id)
        self.assertEqual(retrieved_comment.body, 'Test')

        # Update
        retrieved_comment.body = 'Updated Test'
        retrieved_comment.save()

        updated_comment = PBTComment.objects.get(id=comment.id)
        self.assertEqual(updated_comment.body, 'Updated Test')

        # Delete
        updated_comment.delete()

        with self.assertRaises(PBTComment.DoesNotExist):
            PBTComment.objects.get(id=comment.id)
