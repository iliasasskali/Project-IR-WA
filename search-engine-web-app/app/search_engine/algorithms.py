import nltk
nltk.download('stopwords')
import collections
import math
import re
import string
from array import array
from collections import defaultdict
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

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

# 3. Apply a TF-IDF ranking to your results.
def create_index_tfidf(lines, num_documents):
    """
    Implement the inverted index and compute tf, df and idf
    
    Argument:
    lines -- collection of tweets
    num_documents -- total number of tweets
    
    Returns:
    index - the inverted index (implemented through a Python dictionary) containing terms as keys and the corresponding
    list of document these keys appears in (and the positions) as values.
    tf - normalized term frequency for each term in each document
    df - number of documents each term appear in
    idf - inverse document frequency of each term
    """

    index = defaultdict(list)
    tf = defaultdict(list)  # term frequencies of terms in documents
    df = defaultdict(int)  # document frequencies of terms in the corpus
    tweet_index = defaultdict(str)
    idf = defaultdict(float)

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
        terms = build_terms(tweet)
        
        # Store tweet info in the dictonary to retrieve it faster when searching
        tweet_index[tweetId] = {}
        tweet_index[tweetId]["tweet"] = tweet
        tweet_index[tweetId]["username"] = username
        tweet_index[tweetId]["date"] = date
        tweet_index[tweetId]["hashtags"] = hashtags
        tweet_index[tweetId]["likes"] = likes
        tweet_index[tweetId]["retweets"] = retweets
        tweet_index[tweetId]["url"] = url

        current_page_index = {}
        for position, term in enumerate(terms):
            try:
                # if the term is already in the dict append the position to the corresponding list
                current_page_index[term][1].append(position)
            except:
                # Add the new term as dict key and initialize the array of positions and add the position
                current_page_index[term]=[tweetId, array('I',[position])]

        # Normalize term frequencies
        norm = 0
        for term, posting in current_page_index.items():
            norm += len(posting[1]) ** 2
        norm = math.sqrt(norm)

        # Calculate the tf and df weights
        for term, posting in current_page_index.items():
            tf[term].append(np.round(len(posting[1])/norm,4))
            df[term] += 1 # increment DF for current term

        # Merge the current page index with the main index
        for term_page, posting_page in current_page_index.items():
            index[term_page].append(posting_page)

        # Compute IDF following the formula (3) above. HINT: use np.log
        for term in df:
            idf[term] = np.round(np.log(float(num_documents/df[term])), 4)

    return index, tf, df, idf, tweet_index


def rank_documents(terms, docs, index, idf, tf, tweet_index):
    """
    Perform the ranking of the results of a search based on the tf-idf weights
    
    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies
    tweet_index -- mapping between page id and page title
    
    Returns:
    Print the list of ranked documents
    """

    doc_vectors = defaultdict(lambda: [0] * len(terms))
    query_vector = [0] * len(terms)

    # compute the norm for the query tf
    query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query. 

    query_norm = sum(query_terms_count.values())
    for termIndex, term in enumerate(terms):  # termIndex is the index of the term in the query
        if term not in index:
            continue

        ## Compute tf*idf(normalize TF as done with documents)
        query_vector[termIndex] = query_terms_count[term] / query_norm * idf[term] 

        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):           
            if doc in docs:
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]

    # Calculate the score of each doc 
    # compute the cosine similarity between queyVector and each docVector:
    doc_scores=[[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items() ]
    doc_scores.sort(reverse=True)
    
    result_docs = [x[1] for x in doc_scores]

    """if len(result_docs) == 0:
        print("No results found, try again")
        query = input()
        docs = search_tf_idf(query, index)"""

    return result_docs
