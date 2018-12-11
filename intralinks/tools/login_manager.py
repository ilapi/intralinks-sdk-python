import os
import json
import intralinks.api.v1
import intralinks.api.v2
import intralinks.tools.notebooks_goodies

class LoginManager:
    def __init__(self, il, wm=None):
        self.il = il
        self.wm = wm if wm is not None else intralinks.tools.notebooks_goodies.WidgetManager()
        self.api_configs = self.load_api_configs()

    def set_api_client(self, api_config):
        api_config = api_config.copy()
        api_version = api_config.pop('version')

        if 'session' in api_config and 'config' in api_config:
            session_data = api_config['session']
            config_data = api_config['config']
            
        else:
            session_data = None
            config_data = api_config
        
        if api_version == 1:
            session = intralinks.api.v1.Session(**session_data) if session_data is not None else None
            config = intralinks.api.v1.Config(**config_data)
            
        elif api_version == 2:
            config_data.pop('mode', None)
            session = intralinks.api.v2.Session(**session_data) if session_data is not None else None
            config = intralinks.api.v2.Config(**config_data)
        
        self.il.api_client = intralinks.api.ApiClient(config=config, session=session)
    
    def get_session_data(self, email, password, secure_id):
        secure_id_callback = lambda:secure_id if secure_id is not None and secure_id != '' else None
        self.il.login(email, password, secure_id_callback=secure_id_callback, end_other_sessions=True)
        
        session_data = {
            'session':dict(self.il.api_client.session.__dict__), 
            'config':dict(self.il.api_client.config.__dict__), 
            'version':1 if isinstance(self.il.api_client.config, intralinks.api.v1.Config) else 2
        }
        
        if 'password' in session_data['session']:
            del session_data['session']['password']
        
        if 'is_already_logged_in' in session_data['session']:
            del session_data['session']['is_already_logged_in']

        return session_data
    
    def save_session_data(self, session_data, file_path='data/current_session.json'):
        if not os.path.exists('data'):
            os.makedirs('data')
            
        with open(file_path, 'w') as fp:
            json.dump(session_data, fp)
    
    def load_session_data(self, file_path='data/current_session.json'):
        session_data = None

        with open(file_path, 'r') as fp:
            session_data = json.load(fp)
            
            if 'is_secureid_required' in session_data['session']:
                del session_data['session']['is_secureid_required']

        return session_data

    def load_api_configs(self, folder='api_keys'):
        api_configs = []

        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                if f.lower().endswith('.json'):
                    with open(os.path.join(dirpath, f), 'r') as f:
                        api_configs.append(json.load(f))
        
        if len(api_configs) == 0:
            error_message = """Missing API Config files.

Please create a folder "api_keys" and add at least one JSON file (with the .json extension) containing:

    {
        "version":2,
        "base_url":"https://api.intralinks.com",
        "mode":"client_credentials",
        "client_id":"<your client id / consumer key>",
        "client_secret":"<your client secret / consumer secret>"
    }

Where the JSON fields are:
* version: the API version your Key relates to (typically 2)
* base_url: the API server, typically:
    "https://api.intralinks.com" for the Production environment
    "https://test-api.intralinks.com" for the Test environment
* mode: the authentication mode associated to your Key. The supported values are:
    "authcode"
    "client_credentials"
* client_id (when version = 2)
* client_secret (when version = 2)
* api_key (when version = 1)
* client (when version = 1)

"""
            print(error_message)
            raise Exception(error_message)

        return api_configs

    def api_config_description(self, config):
        if 'description' in config:
            return config['description']
        
        else:
            m = {'services':'prod', 'api':'prod', 'test-api':'test'}
            
            server = config['base_url'][len('https://'):].split('.')[0]
            
            if server in m:
                server = m[server]
            
            version = int(config['version'])
            mode = 'client_credentials' if version == 1 else config['mode']
            
            hash_part = config['client_id'][:4] if version == 2 else config['api_key'][:4]
            
            return '{} - v{} - {} - {}'.format(server, version, mode, hash_part)

class LoginManagerUI:
    def __init__(self, login_manager=None):
        self.login_manager = login_manager
        self.wm = intralinks.tools.notebooks_goodies.WidgetManager()
    
    def _action_login(self, api_config_key, email_key, password_key, secure_id_key, status_key):
        api_config = self.wm[api_config_key].value.copy()

        self.login_manager.set_api_client(api_config)

        if self.login_manager.il.api_client is None:
            self.wm[status_key].value = 'Wrong API Config'
            return
        
        email = self.wm[email_key].value
        password = self.wm[password_key].value   
        secure_id = self.wm[secure_id_key].value

        self.wm[status_key].value = 'Login in...'

        session_data = self.login_manager.get_session_data(email, password, secure_id)
            
        self.wm[status_key].value = str(session_data)
        
        self.login_manager.save_session_data(session_data)

    def _action_load_session(self, status_key):
        session_data = self.login_manager.load_session_data()

        if session_data is None:     
            self.wm[status_key].value = 'Impossible to load session data'  

        else:     
            self.login_manager.set_api_client(session_data)
            self.wm[status_key].value = str(session_data)

    def login_panel(self, with_secure_id=False, email=None, password=None):
        api_config_options = [
            (self.login_manager.api_config_description(config), config) 
            for config in self.login_manager.api_configs
        ]

        self.wm.Dropdown(description='API Config', options=api_config_options, value=api_config_options[0][1], key='api.config')
        self.wm.Text(description='Email', value=email, key='login.email')
        self.wm.Password(description='Password', value=password, key='login.password')
        self.wm.Text(description='Secure ID', key='login.secureid')    
        self.wm.Button(description='Login', action=lambda b: self._action_login('api.config', 'login.email', 'login.password', 'login.secureid', 'login.status'), key='login.button')
        self.wm.Label(key='login.status')
        
        components = []
        
        if len(self.login_manager.api_configs) > 1:
            components.append('api.config')
        
        components.append('login.email')
        components.append('login.password')
        
        if with_secure_id:
            components.append('login.secureid')
        
        components.append('login.button')
        components.append('login.status')

        self.wm.VBox('|'.join(components), key='login.panel', description='Login')

        self.wm.Button(description='Load current session', action=lambda b: self._action_load_session('load_session.status'), key='load_session.button')
        self.wm.Label(key='load_session.status')

        self.wm.VBox('load_session.button|load_session.status', key='load_session.panel', description='Load session')

        return self.wm.Tab('login.panel|load_session.panel')