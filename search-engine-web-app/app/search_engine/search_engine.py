import app.search_engine.algorithms as algorithms
import app.core.utils as utils
import pickle

def build_tweets(tweets, ranked_docs, search_query):
    ranked_tweets = []
    for ranking, ranked_tweet in enumerate(ranked_docs):
        tweet = tweets[ranked_tweet]
        ranked_tweets.append(TweetInfo(
            tweet.id,
            tweet.text,
            tweet.username,
            tweet.date,
            f"doc_details?id={tweet.id}&query={search_query}&pos={ranking + 1}",
            tweet.hashtags,
            tweet.likes,
            tweet.retweets,
            tweet.twitterUrl,
            ranking
        ))

    return ranked_tweets

def load_or_create_index_tfidf(lines):
    try:
        index, tf, df, idf = pickle.load(open("inputs/index_tfidf.pickle", "rb"))
        return index, tf, df, idf 
    except:
        index, tf, df, idf = algorithms.create_index_tfidf(lines, len(lines))
        pickle.dump((index, tf, df, idf), open("inputs/index_tfidf.pickle", "wb"))
        return index, tf, df, idf

class SearchEngine:
    lines = utils.read_json()
    print("Creating index...")
    index, tf, df, idf = load_or_create_index_tfidf(lines)
    print("Index created!")
    print("Loading Tweets...")
    tweets = utils.load_documents_corpus()
    print("Tweets loaded!")

    def search(self, search_query):

        query = utils.build_terms(search_query)
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
        
        # Get max popularity score from the documents containing at least a term
        max_popularity = utils.get_max_popularity_score(docs, self.tweets)

        ranked_docs = algorithms.rank_documents(query, docs, self.index, self.idf, self.tf, max_popularity, self.tweets)

        return build_tweets(self.tweets, ranked_docs, search_query)


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