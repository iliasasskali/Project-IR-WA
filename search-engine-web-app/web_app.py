import os
import json
from json import JSONEncoder

import datetime
import random

import httpagentparser
import nltk
from flask import Flask, render_template, session
from flask import request

from app.analytics.analytics_data import AnalyticsData, Click, User, Query
from app.core import utils
from app.search_engine.search_engine import SearchEngine

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

app = Flask(__name__)


# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'
searchEngine = SearchEngine()
analytics_data = AnalyticsData()
corpus = utils.load_documents_corpus()

@app.route('/')
def search_form():
    print("starting home url /...")

    raw_user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", raw_user_agent)
    user_agent = request.user_agent
    user_ip = request.remote_addr
    user_date = datetime.date.today()
    user_browser = user_agent.browser
    user_platform = user_agent.platform
    url = request.url
    user_id = random.randint(0, 100000)

    if user_id not in analytics_data.fact_users.keys():
        analytics_data.fact_users[user_id] = User(user_ip, user_browser, user_platform, user_date, url)

    print("Remote IP: '{}' - JSON user browser '{}' from platform '{}'".format(user_ip, user_browser, user_platform))
    return render_template('index.html', page_title="Welcome")

@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']

    results = searchEngine.search(search_query)
    found_count = len(results)

    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count, query = search_query)

@app.route('/doc_details', methods=['GET'])
def doc_details():
    # getting request parameters:
    query = request.args["query"]
    clicked_doc_id = int(request.args["id"])
    pos = int(request.args["pos"])
    init_time = request.args.get("time")
    tweet = SearchEngine.tweets[str(clicked_doc_id)]

    print("click in id={}".format(clicked_doc_id))

    # store data in statistics table 1
    if clicked_doc_id in analytics_data.fact_clicks.keys():
        analytics_data.fact_clicks[clicked_doc_id] += 1
    else:
        analytics_data.fact_clicks[clicked_doc_id] = 1

    # store data in statistics table 2
    if clicked_doc_id not in analytics_data.fact_results.keys():
        analytics_data.fact_results[clicked_doc_id] = Click(clicked_doc_id, query, pos)

    # store data in statistics table 3
    if query in analytics_data.fact_queries.keys():
        curr_query = analytics_data.fact_queries[query]
        curr_query.count += 1
    else:
        terms = query.split()
        analytics_data.fact_queries[clicked_doc_id] = Query(query, len(terms), 1)

    print("fact_clicks count for id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))
    return render_template('doc_details.html', tweet = tweet)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []
    print(analytics_data.fact_clicks.keys())
    for doc_id in analytics_data.fact_clicks.keys():
        doc = analytics_data.fact_clicks[doc_id]
        visited_docs.append(doc)
    # simulate sort by ranking
    visited_docs.sort(key=lambda doc: doc, reverse=True)

    queries = []
    for doc_id in analytics_data.fact_queries.keys():
        query = analytics_data.fact_queries[doc_id]
        queries.append(query)

    users = []
    for user_id in analytics_data.fact_users.keys():
        user = analytics_data.fact_users[user_id]
        users.append(user)

    return render_template('dashboard.html', visited_docs=visited_docs, queries=queries, users=users)

@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port="8088", host="0.0.0.0", threaded=False, debug=True)
