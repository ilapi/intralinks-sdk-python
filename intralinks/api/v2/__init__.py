class Config:
    def __init__(self, base_url=None, client_id=None, client_secret=None):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

    def _as_str(self, s):
        return "'{}'".format(s) if s is not None else "None"

    def _as_int(self, s):
        return str(s) if s is not None else "None"

    def __repr__(self):
        return "intralinks.api.v2.Config(base_url={}, client_id={}, client_secret={})".format(
            self._as_str(self.base_url), 
            self._as_str(self.client_id), 
            self._as_str(self.client_secret), 
        )

class Session:
    def __init__(self, access_token=None, refresh_token=None, timestamp=None, email=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.timestamp = timestamp
        self.email = email

    def apply(self, headers, cookies):
        if self.access_token:
            headers['Authorization'] = 'Bearer {}'.format(self.access_token)

    def _as_str(self, s):
        return "'{}'".format(s) if s is not None else "None"

    def __repr__(self):
        return "intralinks.api.v2.Session(access_token={}, refresh_token={}, timestamp={})".format(
            self._as_str(self.access_token),
            self._as_str(self.refresh_token),
            self._as_int(self.timestamp),
        )