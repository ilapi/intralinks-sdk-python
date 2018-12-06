import IPython
import base64
import ipywidgets 
import IPython.display
import pandas as pd
import pandas.io.json

def table(data, first_columns=[], drop_columns=[]):
    data = data.copy()

    for d in data:
        if 'customFields' in d:
            fields = d['customFields']['field']
            if not isinstance(fields, list):
                fields = [fields]
                
            for f in fields:
                d['customField.{}'.format(f['id'])] = f['value']

            del d['customFields']

    df = pd.DataFrame(pandas.io.json.json_normalize(data))
    
    columns = df.columns.tolist()
    columns = [c for c in first_columns if c in set(columns)] + [c for c in columns if c not in set(first_columns) and c not in set(drop_columns)]
    
    return df[columns]

def create_code_cell(code='', where='below'):
    """Create a code cell in the IPython Notebook.

    Parameters
    code: unicode
        Code to fill the new code cell with.
    where: unicode
        Where to add the new code cell.
        Possible values include:
            at_bottom
            above
            below"""
    encoded_code = base64.b64encode(code.encode()).decode()
    display(IPython.display.Javascript("""
        var code = IPython.notebook.insert_cell_{0}('code');
        code.set_text(atob("{1}"));
    """.format(where, encoded_code)))

class ProgressBar:
    def __init__(self, items=None, count=None):
        self.progress_bar = ipywidgets.IntProgress(min=0, max=len(items) if items else count)
        self.status_bar = ipywidgets.Label()
    
        IPython.display.display(self.progress_bar)
        IPython.display.display(self.status_bar)
     
    def state(self, step=None, message=None):
        if step:
            self.progress_bar.value += step

        if message:
            self.status_bar.value = message

class WidgetManager:
    def __init__(self):
        self.widgets = dict()
    
    def register_widget(self, w, key=None, description=None):
        if key:
            self.widgets[key] = (w, description)
            
        return w
    
    def Label(self, value=None, key=None): # NOSONAR
        w = ipywidgets.widgets.Label(value=value)
        return self.register_widget(w, key)
    
    def Text(self, description, value=None, key=None): # NOSONAR
        w = ipywidgets.widgets.Text(description=description, value=value)
        return self.register_widget(w, key)
    
    def Password(self, description, value=None, key=None): # NOSONAR
        w = ipywidgets.widgets.Password(description=description, value=value)
        return self.register_widget(w, key)
    
    def Dropdown(self, description, options, value=None, key=None): # NOSONAR
        w = ipywidgets.widgets.Dropdown(description=description, options=options, value=value)
        return self.register_widget(w, key)

    def Button(self, description, action=None, key=None): # NOSONAR
        w = ipywidgets.widgets.Button(description=description)
        w.on_click(action)
        return self.register_widget(w, key)
    
    def RadioButtons(self, description='', options=None, key=None): # NOSONAR
        w = ipywidgets.widgets.RadioButtons(description=description, options=options)
        return self.register_widget(w, key)
    
    def IntProgress(self, description='', key=None): # NOSONAR
        w = ipywidgets.widgets.IntProgress(description=description)
        return self.register_widget(w, key)

    def _key_list(self, keys):
        if isinstance(keys, str):
            keys = keys.split('|')
            
        return keys
    
    def VBox(self, keys, description=None, key=None): # NOSONAR
        w = ipywidgets.widgets.VBox([self[k] for k in self._key_list(keys)])
        return self.register_widget(w, key, description)
    
    def _populate_named_container(self, w, keys):
        children = [self.widgets[k] for k in self._key_list(keys)]
        
        w.children = [c[0] for c in children]
        
        for i, c in enumerate(children):
            w.set_title(i, c[1])
    
    def Tab(self, keys, description=None, key=None): # NOSONAR
        w = ipywidgets.widgets.Tab()
        self._populate_named_container(w, keys)
        return self.register_widget(w, key, description)
    
    def Accordion(self, keys, description=None, key=None): # NOSONAR
        w = ipywidgets.widgets.Accordion()
        self._populate_named_container(w, keys)
        return self.register_widget(w, key, description)

    def __getitem__(self, key):
        return self.widgets[key][0]
        