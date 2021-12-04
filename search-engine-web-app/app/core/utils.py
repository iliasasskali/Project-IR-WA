import json

class Tweet:
    def __init__(self, id, text, username, date, hashtags, likes, retweets, twitterUrl):
        self.id = id
        self.text = text
        self.username = username
        self.date = date
        self.hashtags = hashtags
        self.likes = likes
        self.retweets = retweets
        self.twitterUrl = twitterUrl

def load_documents_corpus():
    """
    Load documents corpus from dataset_tweets_WHO.txt file
    :return:
    """

    # Read json and store the text of each tweet into a list
    
    with open('inputs/dataset_tweets_WHO.txt') as fp:
        lines = json.load(fp)

    docs = {}
    for tweetId in lines:
        full_tweet = lines[str(tweetId)]
        
        tweet_id = full_tweet["id"] # id 
        tweet = full_tweet["full_text"] # Tweet
        username = full_tweet["user"]["screen_name"] # Username
        date = full_tweet["created_at"] # Date
        hashtags = full_tweet["entities"]["hashtags"] # Hashtags
        likes = full_tweet["favorite_count"] # Likes
        retweets = full_tweet["retweet_count"] # Retweets
        url = f"https://twitter.com/{username}/status/{tweet_id}" # Url

        docs[tweetId] = Tweet(tweetId, tweet, username, date, hashtags, likes, retweets, url)
    return docs

# Read json and store the text of each tweet into a list
def read_json(docs_path = 'inputs/dataset_tweets_WHO.txt'):
    with open(docs_path) as fp:
        lines = json.load(fp)

    print("Total number of tweets in the dataset: {}".format(len(lines)))
    return lines