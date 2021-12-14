import json
import random

class AnalyticsData:
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])

    # fact_results is a dictionary with the click done to a document by each query: key = doc id | value = click
    fact_results = dict([])

    # fact_queriesClicks is a dictionary with the query term count: key = query | value = term counter
    fact_queries = dict([])

     # fact_users is a dictionary with the users info: key = user_id | value = User()
     fact_users = dict([])


class Click:
    def __init__(self, doc_id, query, pos):
        self.doc_id = doc_id
        self.query = query
        self.pos = pos

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

class Query:
    def __init__(self, query, length, count):
        self.query = query
        self.length = length
        self.count = count

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

class User:
    def __init__(self, ip, browser, platform, date, time, city, country):
        self.ip = ip
        self.browser = browser
        self.platform = platform
        self.date = date
        self.time = time
        self.city = city
        self.country = country

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)