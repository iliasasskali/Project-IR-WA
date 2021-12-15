import json

class AnalyticsData:
    # fact_results is a dictionary with the click done to a document by each query: key = doc id | value = click
    fact_results = dict([])

    # fact_queriesClicks is a dictionary with the query term count: key = query | value = term counter
    fact_queries = dict([])

     # fact_users is a dictionary with the users info: key = user_id | value = User()
    fact_users = dict([])


class Click:
    def __init__(self, doc_id, query, pos, count):
        self.doc_id = doc_id
        self.query = query
        self.pos = pos
        self.count = count

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
    def __init__(self, ip, browser, platform, date, url):
        self.ip = ip
        self.browser = browser
        self.platform = platform
        self.date = date
        self.url = url

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)