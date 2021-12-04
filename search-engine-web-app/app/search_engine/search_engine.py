import app.search_engine.algorithms as algorithms
import app.core.utils as utils

def build_tweets(tweets, ranked_docs):
    ranked_tweets = []
    for ranking, ranked_tweet in enumerate(ranked_docs):
        for tweet in tweets:
            if tweet.id == ranked_tweet:
                ranked_tweets.append(TweetInfo(
                    tweet.id,
                    tweet.text,
                    tweet.username,
                    tweet.date,
                    f"doc_details?id={tweet.id}&param1=1&param2=2",
                    tweet.hashtags,
                    tweet.likes,
                    tweet.retweets,
                    tweet.twitterUrl,
                    ranking
                ))

    return ranked_tweets


class SearchEngine:
    lines = utils.read_json()
    print("Creating index...")
    index, tf, df, idf, tweet_index = algorithms.create_index_tfidf(lines, len(lines))
    print("Index created!")
    print("Loading Tweets...")
    tweets = utils.load_documents_corpus()
    print("Tweets loaded!")

    def search(self, search_query):
        query = algorithms.build_terms(search_query)
        docs = set()
        for term in query:
            try:
                # store in term_docs the ids of the docs that contain "term"
                term_docs = [posting[0] for posting in self.index[term]]

                # docs = docs Union term_docs
                docs = docs.union(term_docs)
            except:
                # term is not in index
                pass
        docs = list(docs)
        ranked_docs = algorithms.rank_documents(query, docs, self.index, self.idf, self.tf, self.tweet_index)

        return build_tweets(self.tweets, ranked_docs)

class TweetInfo:
    def __init__(self, id, text, username, date, url, hashtags, likes, retweets, twitterUrl, ranking):
        self.id = id
        self.text = text
        self.username = username
        self.date = date
        self.hashtags = hashtags
        self.likes = likes
        self.retweets = retweets
        self.twitterUrl = twitterUrl
        self.url = url
        self.ranking = ranking