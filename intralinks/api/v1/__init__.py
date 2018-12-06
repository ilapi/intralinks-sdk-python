import requests
import intralinks.api

class Config:
    def __init__(self, base_url=None, api_key=None, client=None, session_id=None, timestamp=None):
        self.base_url = base_url
        self.api_key = api_key
        self.client = client

    def _as_str(self, s):
        return "'{}'".format(s) if s is not None else "None"

    def __repr__(self):
        return "intralinks.api.v1.Config(base_url={}, api_key={}, client={})".format(
            self._as_str(self.base_url), 
            self._as_str(self.api_key), 
            self._as_str(self.client), 
        )    

class Session:
    def __init__(self,  session_id=None, timestamp=None, email=None):
        self.session_id = session_id
        self.timestamp = timestamp
        self.email = email
    
    def apply(self, headers, cookies):
        if self.session_id:
            cookies['ssoGlobalSessionID'] = self.session_id

    def _as_str(self, s):
        return "'{}'".format(s) if s is not None else "None"

    def _as_int(self, s):
        return str(s) if s is not None else "None"

    def __repr__(self):
        return "intralinks.api.v1.Session(session_id={}, timestamp={})".format(
            self._as_str(self.session_id),
            self._as_int(self.timestamp),
        )
