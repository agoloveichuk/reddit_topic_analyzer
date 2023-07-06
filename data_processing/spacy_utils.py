from datetime import datetime, timedelta
import spacy
import collections

from gensim.models.phrases import Phrases, ENGLISH_CONNECTOR_WORDS
from textblob import TextBlob
from data_extraction.models import DailyBestPost, DBPComment, PostByTopic, PBTComment
from data_processing.models import NamedEntity
from spacytextblob.spacytextblob import SpacyTextBlob
from collections import Counter
from gensim.models.phrases import Phrases, Phraser

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")

def update_daily_named_entities():
    # return all entities even with topic FIX 
    topic = ''
    NamedEntity.objects.filter(topic='').all().delete()  # clear existing entities
    entities = []
    for post in DailyBestPost.objects.all():
        doc = nlp(post.title + ' ' + post.body)
        entities += [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ('PERSON', 'ORG', 'PRODUCT', 'EVENT')]
        for comment in DBPComment.objects.all():
            doc = nlp(comment.body)
            entities += [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ('PERSON', 'ORG', 'PRODUCT', 'EVENT')]
    counter = collections.Counter(entities)
    for (name, label), freq in counter.items():
        entity, created = NamedEntity.objects.get_or_create(name=name, label=label, topic=topic)
        entity.frequency += freq
        entity.save()

def get_top_daily_entities():
    topic = ''
    update_daily_named_entities()
    entities = NamedEntity.objects.filter(topic=topic).order_by('-frequency')[:3]
    return [(entity.name, entity.frequency) for entity in entities]

def update_named_entities(topic):
    NamedEntity.objects.filter(topic=topic).delete()  # clear existing entities
    entities = []
    for post in PostByTopic.objects.filter(topic=topic):
        doc = nlp(post.title + ' ' + post.body)
        entities += [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ('PERSON', 'ORG', 'PRODUCT', 'EVENT')]
        for comment in PBTComment.objects.filter(topic=topic):
            doc = nlp(comment.body)
            entities += [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ('PERSON', 'ORG', 'PRODUCT', 'EVENT')]
    counter = collections.Counter(entities)
    for (name, label), freq in counter.items():
        entity, created = NamedEntity.objects.get_or_create(name=name, label=label, topic=topic)
        entity.frequency += freq
        entity.save()

def get_top_entities(topic):
    update_named_entities(topic)
    entities = NamedEntity.objects.filter(topic=topic).order_by('-frequency')[:15]
    return [(entity.name, entity.frequency) for entity in entities]

def get_sentiment(text):
    doc = nlp(text)
    sentiment_score = doc._.blob.polarity  
    return sentiment_score

def get_top_phrases(topic):
    all_sentences = []
    if topic == '':
        for post_comment in DBPComment.objects.all():
            doc = nlp(post_comment.body)
            sentences = [sent.text for sent in doc.sents if len(sent) > 1]
            all_sentences.extend(sentences)
    else:
        for post_comment in PBTComment.objects.filter(topic=topic):
            doc = nlp(post_comment.body)
            sentences = [sent.text for sent in doc.sents if len(sent) > 1]
            all_sentences.extend(sentences)

    print("All sentences:", all_sentences)

    phrases = Phrases(all_sentences, min_count=5, threshold=10, connector_words=ENGLISH_CONNECTOR_WORDS)
    phraser = Phraser(phrases)
    print("Phrases detected:", phraser.phrasegrams)

    top_phrases = {}
    for phrase, freq in phraser.phrasegrams.items():
        sentiment = get_sentiment(phrase)
        top_phrases[phrase] = {"frequency": freq, "sentiment": sentiment}
    
    return top_phrases

def analyze_sentiment_scores(data_range, topic):
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
        sentiment = get_sentiment(comment.body)
        comment_sentiments.append({
            'sentiment': sentiment,
        })

    positive_threshold = 0.2
    negative_threshold = -0.2

    positive_count = sum(score['sentiment'] > positive_threshold for score in comment_sentiments)
    negative_count = sum(score['sentiment'] < negative_threshold for score in comment_sentiments)
    neutral_count = len(comment_sentiments) - positive_count - negative_count

    sentiment_scores = [score['sentiment'] for score in comment_sentiments]
    average_score = sum(sentiment_scores) / len(sentiment_scores)

    sentiment_scores_2 = [score['sentiment'] for score in comment_sentiments if score['sentiment'] != 0]
    average_score_2 = sum(sentiment_scores_2) / len(sentiment_scores_2) if sentiment_scores_2 else 0.0

    sentiment_category = None
    if positive_count > negative_count:
        sentiment_category = 'positive'
    elif positive_count < negative_count:
        sentiment_category = 'negative'
    else:
        sentiment_category = 'neutral'

    sentiment_results = {
        'sentiment_category': sentiment_category,
        'average_score': average_score,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'average_score_2': average_score_2,
    }   

    return sentiment_results

def analyze_sentiment_scores_posts(data_range, topic):
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
            created_utc__gte=start_date,
            topic=topic
        )
        comments = PBTComment.objects.filter(
            created_utc__gte=start_date,
            topic=topic
        )

    sentiment_results = []
    for post in posts:
        post_comments = comments.filter(post=post)
        comment_sentiments = []
        for comment in post_comments:
            sentiment = get_sentiment(comment.body)
            comment_sentiments.append({
                'sentiment': sentiment,
            })

        positive_threshold = 0.2
        negative_threshold = -0.2

        positive_count = sum(score['sentiment'] > positive_threshold for score in comment_sentiments)
        negative_count = sum(score['sentiment'] < negative_threshold for score in comment_sentiments)
        neutral_count = len(comment_sentiments) - positive_count - negative_count

        sentiment_scores = [score['sentiment'] for score in comment_sentiments]
        average_score = sum(sentiment_scores) / len(sentiment_scores)

        sentiment_scores_2 = [score['sentiment'] for score in comment_sentiments if score['sentiment'] != 0]
        average_score_2 = sum(sentiment_scores_2) / len(sentiment_scores_2) if sentiment_scores_2 else 0.0


        sentiment_category = None
        if positive_count > negative_count:
            sentiment_category = 'positive'
        elif positive_count < negative_count:
            sentiment_category = 'negative'
        else:
            sentiment_category = 'neutral'

        sentiment_result = {
            'post_title': post.title,
            'post_url' : post.url,
            'sentiment_category': sentiment_category,
            'average_score': average_score,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'average_score_2' : average_score_2,
        }
        sentiment_results.append(sentiment_result)

    return sentiment_results



