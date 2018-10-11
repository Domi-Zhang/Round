class UrlSubmitJob(object):
    def __init__(self, url, priority):
        self.url = url
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority
