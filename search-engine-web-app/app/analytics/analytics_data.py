class AnalyticsData:
    fact_clicks = []
    fact_queries = []
    fact_three = []


class Click:
    def __init__(self, doc_id, query, pos):
        self.doc_id = doc_id
        self.query = query
        self.pos = pos
