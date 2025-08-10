import requests

class HttpService:
    def __init__(self):
        self.session = requests.Session()
        
    def get(self, url, params={}):
        return self.session.get(url, params=params )
    
    def post(self, url, data={}):
        return self.session.post(url, data=data)
    
    def put(self, url, data={}):
        return self.session.put(url, data=data)
    
    def delete(self, url, data={}):
        return self.session.delete(url, data=data)
    
    def config_service(self, headers = {}, base_url = "" ):
        self.session.headers = headers
        self.session.base_url = base_url
        return self
    
