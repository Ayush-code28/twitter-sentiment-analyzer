import tweepy
from textblob import TextBlob
import re

# Your X API v2 Bearer Token
BEARER_TOKEN = 'Your_Bearer_Token'

class TwitterClientV2:
    def __init__(self):
        self.client = tweepy.Client(bearer_token=BEARER_TOKEN)

    def clean_tweet(self, tweet):
        return ' '.join(re.sub(r"(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, max_results=10):
        tweets_data = []
        try:
            response = self.client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=['text'])
            if response.data:
                for tweet in response.data:
                    text = tweet.text
                    sentiment = self.get_tweet_sentiment(text)
                    tweets_data.append({'text': text, 'sentiment': sentiment})
            return tweets_data
        except tweepy.errors.TweepyException as e:
            print("Tweepy Exception:", e)
            return []

def main():
    api = TwitterClientV2()
    tweets = api.get_tweets(query='Adidas', max_results=10)

    ptweets = [t for t in tweets if t['sentiment'] == 'positive']
    ntweets = [t for t in tweets if t['sentiment'] == 'negative']
    neutrals = [t for t in tweets if t['sentiment'] == 'neutral']

    print(f"Positive tweets: {len(ptweets)} / {len(tweets)}")
    print(f"Negative tweets: {len(ntweets)} / {len(tweets)}")
    print(f"Neutral tweets: {len(neutrals)} / {len(tweets)}")

    print("\nSome Positive tweets:")
    for t in ptweets[:5]:
        print("-", t['text'])

    print("\nSome Negative tweets:")
    for t in ntweets[:5]:
        print("-", t['text'])

if __name__ == "__main__":
    main()
