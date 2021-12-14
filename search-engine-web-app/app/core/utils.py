import json
import re
import string
from nltk.stem import PorterStemmer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

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
    max_popularity = 0 # Popularity is 0.4*likes + 0.6*retweets, we want to find max to normalize
    for tweetId in lines:
        full_tweet = lines[str(tweetId)]
        
        tweet_id = full_tweet["id"] # id 
        tweet = full_tweet["full_text"] # Tweet
        username = full_tweet["user"]["screen_name"] # Username
        date = full_tweet["created_at"] # Date
        hashtags = list(map(lambda x: f"#{x['text']}", full_tweet["entities"]["hashtags"])) # Hashtags
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

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)

url_pattern = re.compile(r'https?://\S+|www\.\S+')

def remove_urls(line):
    return url_pattern.sub(r'', line)

def remove_emojis(line):
    return emoji_pattern.sub(r'', line)

def build_terms(line):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    line = line.encode("ascii", "ignore") # Remove unicode characters
    line = line.decode()
    line = line.lower() ## Transform to lowercase
    line = remove_emojis(line) ## Remove emojis, before tokenizing to delete emojis not separated by space with a word
    line = remove_urls(line) ## Remove urls
    line = line.split() ## Tokenize the text to get a list of terms
    line = [w for w in line if w not in stop_words]  ## eliminate the stopwords
    line = [w for w in line if w[0]!='&' and w[-1]!=';'] ## Remove HTML symbol entity codes
    line = [w.strip(string.punctuation.replace('#', '').replace('@', '')) for w in line] ## Remove punctuation except # and @
    line = [stemmer.stem(w) for w in line if w!=''] ## perform stemming and remove empty words
    return line

def get_max_popularity_score(docs, tweets):
    max_popularity = 0
    for doc in docs:
        popularity = (0.4*tweets[doc].likes) + (0.6*tweets[doc].retweets)
        if (popularity > max_popularity): max_popularity = popularity
    return max_popularity