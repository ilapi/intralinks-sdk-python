import re
import json
import concurrent.futures
import pandas as pd
import datetime
import intralinks.utils.dates
from intralinks.utils.data import entity_to_dict, get_node_as_list
import ipywidgets
from intralinks.tools.notebooks_goodies import create_code_cell, WidgetManager
import traceback

INTRALINKS_USER_KEYS = {
    'userId',
    'emailId',

    'firstName',
    'firstNameSort',
    'lastName',
    'lastNameSort',

    'mobilePhone',
    'officePhone',
    'fax',

    'address1',
    'address2',
    'postalCode',
    'city',
    'state',
    'country',

    'jobTitle',
    'title',
    'organization',
    'organizationId',
    'organizationSort',

    'timeZone',
    'timeZoneOffset',

    'functionalArea',
    'industry',

    'isAdminUser',
    'isLinkedUp',
    'isPlaceholderUser',

    'lastLoginDate',

    'userLocale'
}

class UserManager:
    def __init__(self, il=None, use_custom_fields=False, use_removed_exchange_members=False, max_workers=5):
        self.il = il
        self.configuration = None
        self.max_worker = max_workers

        self.use_custom_fields = use_custom_fields
        self.use_removed_exchange_members = use_removed_exchange_members

        self.reference_user = None

        self.intralinks_users = None
        self.exchanges = None
        self.field_definitions = None
        self.groups = None
        self.exchange_members = None
        self.removed_exchange_members = None
        self.group_members = None

        self.dataframe = None
    
    def _categorize_intralinks_user(self, u):
        u['domain'] = u['emailId'].lower().split('@')[1]
        u['email'] = u['emailId'].lower()

    def categorize_data(self):
        """
        Options to categorize data:
        - use naming conventions
        - use an external datasource
        - use exchange's description, group's note
        - use custom fields
        """
        for u in self.intralinks_users:
            self._categorize_intralinks_user(u)

        if self.configuration:
            for u in self.exchange_members:
                self.configuration.categorize_user(u)

            for e in self.exchanges:
                self.configuration.categorize_exchange(e)

            for g in self.groups:
                self.configuration.categorize_group(g)

    def _prepare_entity(self, prefix, entity, skip=None):
        new_entity = dict()
        
        for k in entity:
            if skip is not None and k in skip:
                continue

            elif k == 'customFields':
                custom_fields = get_node_as_list(entity, ['customFields', 'field'])
                
                for c in custom_fields:
                    new_entity['{}.cf.{}'.format(prefix, c['id'])] = c['value']

            elif k in {'createdOn', 'lastModifiedOn', 'firstAccessed', 'lastAccessedOn', 'lastAlertSentDate'}:
                new_entity['{}.{}'.format(prefix, k)] = intralinks.utils.dates.to_date(entity[k]['milliseconds'])

            else:
                new_entity['{}.{}'.format(prefix, k)] = entity[k]
        
        return new_entity

    def prepare_dataframe(self):
        SKIP_INTRALINKS_USER_KEYS = {'firstNameSort', 'lastNameSort', 'organizationSort', 'mobilePhone', 'fax', 'address1', 'address2', 'postalCode', 'city', 'state', 'country', 'title', 'functionalArea', 'industry'}
        SKIP_EXCHANGE_KEYS = {'createdBy', 'createdOn', 'lastModifiedBy', 'lastModifiedOn', 'pvpEnabled', 'securityLevel', 'type', 'version'}
        SKIP_GROUP_KEYS = {'buyerGroupDetails', 'createdBy', 'createdOn', 'lastModifiedBy', 'lastModifiedOn', 'ftsEnabled', 'groupMemberCount', 'groupMembers', 'version', 'exchange_id'}
        SKIP_EXCHANGE_MEMBER_KEYS = {'version', 'cgFlag', 'title', 'groups', 'exchange_id', 'domain', 'createdBy', 'lastModifiedBy', 'userId'}

        exchanges_by_id = {e['id']:self._prepare_entity('exchange', e, skip=SKIP_EXCHANGE_KEYS) for e in self.exchanges}
        intralinks_users_by_id = {u['userId']:self._prepare_entity('intralinks_user', u, skip=SKIP_INTRALINKS_USER_KEYS) for u in self.intralinks_users}
        exchange_members_by_id = {m['id']:self._prepare_entity('exchange_member', m, skip=SKIP_EXCHANGE_MEMBER_KEYS) for m in self.exchange_members}
        groups_by_id = {g['id']:self._prepare_entity('group', g, skip=SKIP_GROUP_KEYS) for g in self.groups}

        rows = []

        for e in self.exchanges:
            d = {'row_type':'EXCHANGE'}
            d.update(exchanges_by_id[e['id']])
            rows.append(d)

        for m in self.exchange_members:
            d = {'row_type':'EXCHANGE_MEMBER'}
            d.update(intralinks_users_by_id[m['userId']])
            d.update(exchange_members_by_id[m['id']])
            d.update(exchanges_by_id[m['exchangeId']])
            rows.append(d)

        for g in self.groups:
            d = {'row_type':'GROUP'}
            d.update(groups_by_id[g['id']])
            d.update(exchanges_by_id[g['exchangeId']])
            rows.append(d)

        for m in self.group_members:
            d = {'row_type':'GROUP_MEMBER'}
            d.update(intralinks_users_by_id[m['userId']])
            d.update(exchange_members_by_id[m['workspaceUserId']])
            d.update(groups_by_id[m['workspaceGroupId']])
            d.update(exchanges_by_id[m['exchangeId']])
            rows.append(d)    
        
        self.dataframe = pd.DataFrame(pd.io.json.json_normalize(rows))
    
    def load_exchanges_from_intralinks(self, email=None, is_manager=None):
        if email is None:
            if re.match('.*\./*@intralinks.com', self.il.api_client.session.email):
                raise Exception()

            self.reference_user = self.il.api_client.session.email
            self.exchanges = self.il.get_exchanges(is_manager=is_manager)

        else:
            self.reference_user = email
            user = self.il.get_user_account(email)[0]
            self.exchanges = self.il.get_exchanges(user_id=user['userId'])
    
    def _split_intralinks_users_from_exchange_members(self, exchange_members_with_details, intralinks_user_ids):
        exchange_members = []

        for m in exchange_members_with_details:
            if m['userId'] not in intralinks_user_ids:
                u = {k:m[k] for k in m if k in INTRALINKS_USER_KEYS}
                intralinks_user_ids.add(m['userId'])
                self.intralinks_users.append(u)
            
            m_cleaned = {k:m[k] for k in m if k == 'userId' or k not in INTRALINKS_USER_KEYS}
            exchange_members.append(m_cleaned)
        
        return exchange_members

    def log(self, operation, count=None, step=None):
        pass

    def load_exchange_data(self, e):
        result = None

        try:
            if self.il.enter_exchange(e, accept_splash=True) != 'ALLOW':
                return None

            e.update(self.il.get_exchange(e))

            if self.use_custom_fields:
                field_definitions = self.il.get_field_definitions(e)

                for f in field_definitions:
                    f['exchangeId'] = e['id']

            else:
                field_definitions = []

            exchange_members = self.il.get_exchange_members(e)  

            for m in exchange_members:
                m['exchangeId'] = e['id']

            if self.use_removed_exchange_members:
                removed_exchange_members = self.il.get_removed_exchange_members(e)

                for m in removed_exchange_members:
                    m['exchangeId'] = e['id']
            else:
                removed_exchange_members = []

            groups, group_members = self.il.get_groups_and_members(e)
            
            for g in groups:
                g['exchangeId'] = e['id']
                
            for m in group_members:
                m['exchangeId'] = e['id']

            result = {
                'field_definitions':field_definitions,
                'exchange_members':exchange_members,
                'removed_exchange_members':removed_exchange_members,
                'groups':groups,
                'group_members':group_members
            }
            
        except:
            traceback.print_exc()
            print('!!! Error with exchange {}'.format(e['id']))
            self.log('load_users_and_groups_from_intralinks', style='warning')
            #self.il.diagnose()
        
        self.log('load_users_and_groups_from_intralinks', step=e)

        return result

    def load_users_and_groups_from_intralinks(self, callback=None):
        self.intralinks_users = []
        self.field_definitions = []
        self.groups = []
        self.exchange_members = []
        self.removed_exchange_members = []
        self.group_members = []

        intralinks_user_ids = set()

        exchanges = [e for e in self.exchanges if e['type'] != 'IL5']

        self.log('load_users_and_groups_from_intralinks', count=len(exchanges), style='')

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_worker) as executor:
            results = executor.map(lambda e: self.load_exchange_data(e), exchanges)
            
            for data in results:
                if data is not None:
                    exchange_members = self._split_intralinks_users_from_exchange_members(data['exchange_members'], intralinks_user_ids)

                    self.field_definitions.extend(data['field_definitions'])
                    self.exchange_members.extend(exchange_members)
                    self.removed_exchange_members.extend(data['removed_exchange_members'])
                    self.groups.extend(data['groups'])
                    self.group_members.extend(data['group_members'])
    
    def save_to_file(self, f):
        with open(f, 'w') as outfile:
            json.dump({
                'intralinks_users':self.intralinks_users,
                'exchanges':self.exchanges, 
                'field_definitions':self.field_definitions,
                'exchange_members':self.exchange_members, 
                'removed_exchange_members':self.removed_exchange_members, 
                'groups':self.groups, 
                'group_members':self.group_members
            }, outfile)

    def load_from_file(self, f):
        with open(f, 'r') as outfile:
            d = json.load(outfile)

            self.exchanges = d['exchanges'] if 'exchanges' in d else []
            self.field_definitions = d['field_definitions'] if 'field_definitions' in d else []
            self.removed_exchange_members = d['removed_exchange_members'] if 'removed_exchange_members' in d else []
            self.groups = d['groups'] if 'groups' in d else []

            if 'exchange_members' in d:
                self.exchange_members = d['exchange_members']
                self.intralinks_users = d['intralinks_users'] if 'intralinks_users' in d else []

            elif 'users' in d:
                exchange_members_with_details = d['users']
                self.intralinks_users = [] # Filled by the next call to self._split_intralinks_users_from_exchange_members
                self.exchange_members = self._split_intralinks_users_from_exchange_members(exchange_members_with_details, set())

            else:
                self.exchange_members = []

            if 'group_members' in d:
                self.group_members = d['group_members']
            elif 'members' in d:
                self.group_members = d['members']
            else:
                self.group_members = []
            
            for o in self.groups + self.exchange_members + self.group_members:
                if 'exchange_id' in o:
                    o['exchangeId'] = o['exchange_id']
                    del o['exchange_id']

    #=========================================================================================

    def get_primary_email(self, email, exchange_id=None):
        user = self.il.get_user_account(email, exchange_id)[0]
        return user['emailId']
    
    #=========================================================================================

    def top_users(self, dataframe=None, min_groups=2):
        """
            Give the list of the users sorted by the number of groups they are member of
            The users with the most groups appear at the top

            Parameters:
            -----------
                dataframe: dataframe
                    the Pandas dataframe to analyse for top users
                min_groups: int, default=2
                    return only the users who are memeber of at least <min_groups> groups
        """

        if dataframe is None:
            dataframe = self.dataframe

        df = dataframe[(~dataframe['intralinks_user.emailId'].isnull())].groupby('intralinks_user.emailId').agg(
            self._columns_in_dataframe(dataframe, {
                'exchange.id':lambda v:v.nunique(dropna=True),
                'group.id':lambda v:v.nunique(dropna=True)
            })
        ).reset_index()
        
        df = df.rename(index=str, columns={
            'intralinks_user.emailId': 'email', 
            'exchange.id': 'exchange_count',
            'group.id': 'group_count'
        })

        if 'group_count' in df:
            df = df[df['group_count'] > min_groups]
        
        return self._sort_values(df, 'group_count', ascending=False)
    
    def _columns_in_dataframe(self, dataframe, collection):
        if isinstance(collection, list):
            return [c for c in collection if c in dataframe]

        elif isinstance(collection, dict):
            return {c:collection[c] for c in collection if c in dataframe}

        else:
            return collection
    
    def _sort_values(self, dataframe, column, ascending):
        if column in dataframe:
            return dataframe.sort_values(column, ascending=ascending)
        else:
            return dataframe

    def top_groups(self, dataframe=None, min_users=10):
        if dataframe is None:
            dataframe = self.dataframe

        df = dataframe[(~dataframe['intralinks_user.emailId'].isnull())].groupby(
            self._columns_in_dataframe(dataframe, [
                'exchange.id', 
                'exchange.workspaceName', 
                'group.id', 
                'group.groupName', 
                'group.list_type', 
                'group.list_id', 
                'group.doc_type'
            ])
        ).agg({
            'exchange_member.id':len, 
            'intralinks_user.domain':lambda v:'|'.join(sorted(v.unique()))
        }).reset_index()

        df = df[df['exchange_member.id'] > min_users]
        
        return self._sort_values(df, 'exchange_member.id', ascending=False)
    
    def top_investors(self, dataframe=None):
        if dataframe is None:
            dataframe = self.dataframe

        df = dataframe[(~dataframe['intralinks_user.emailId'].isnull())].groupby([
            'group.list_id'
        ]).agg({
            'exchange.id':lambda v:len(v.unique()), 
            'group.doc_type':lambda v:len(v.unique()), 
            'intralinks_user.emailId':lambda v:len(v.unique()), 
            'intralinks_user.domain':lambda v:'|'.join(sorted(v.unique()))
        }).reset_index()
        
        return self._sort_values(df, 'exchange.id', ascending=False)
    
    def orphans(self, dataframe=None):
        if dataframe is None:
            dataframe = self.dataframe

        df = dataframe[~dataframe['intralinks_user.emailId'].isnull()].groupby([
            'intralinks_user.emailId', 
            'exchange.id', 
            'exchange.workspaceName', 
            'exchange_member.roleType'
        ]).agg({'group.id':len}).reset_index()

        return df[(df['group.id'] == 1) & (~df['exchange_member.roleType'].isin({'MANAGER_PLUS', 'HIDDEN_MANAGER_PLUS', 'PUBLISHER'}))].pivot_table(
            index='intralinks_user.emailId', 
            columns='exchange.workspaceName', 
            aggfunc={'exchange_member.roleType':lambda v:v.unique()[0]
        }).fillna('')

    def exchanges_for(self, dataframe=None, email=None):
        if dataframe is None:
            dataframe = self.dataframe

        return dataframe[dataframe['intralinks_user.email'] == email.lower()].groupby(['exchange.id', 'exchange.workspaceName']).aggregate({
            'exchange_member.roleType':lambda v: ', '.join(v.unique()),
            'group.id':lambda v: v.nunique(dropna=True)
        })

    def groups_for(self, dataframe=None, email=None, domain=None):
        if dataframe is None:
            dataframe = self.dataframe

        filter2 = None
        
        if email:
            if isinstance(email, str):
                email = [email]
            filter2 = dataframe['intralinks_user.email'].isin({e.lower() for e in email})
        else:
            if isinstance(domain, str):
                domain = [domain]
            filter2 = dataframe['intralinks_user.domain'].isin({d.lower() for d in domain})        

        # all the entries for the specified user
        df1 = dataframe[(~dataframe['group.id'].isnull()) & (filter2)]
        
        # all the associated groups
        group_ids = df1['group.id'].unique()
        
        # all the entries for the associated groups, whatever the user
        df2 = dataframe[(~dataframe['intralinks_user.emailId'].isnull()) & (dataframe['group.id'].isin(group_ids))]
        
        # counting users and domains
        df3 = df2.groupby(
            self._columns_in_dataframe(dataframe, [
                'exchange.id', 
                'exchange.workspaceName', 
                'group.id', 
                'group.groupName', 
                'group.list_type', 
                'group.list_id', 
                'group.doc_type'
            ])
        ).agg(
            self._columns_in_dataframe(dataframe, {
                'exchange_member.roleType':lambda v: ', '.join(v.unique()),
                'intralinks_user.id':len, 
                'intralinks_user.domain':lambda v:'|'.join(sorted(v.unique()))
            })
        )
        
        return df3
    
    def team_for(self, dataframe=None, email=None, domain=None):
        if dataframe is None:
            dataframe = self.dataframe

        filter2 = None
        
        if email:
            if isinstance(email, str):
                email = [email]
            filter2 = dataframe['intralinks_user.email'].isin({e.lower() for e in email})
        else:
            if isinstance(domain, str):
                domain = [domain]
            filter2 = dataframe['intralinks_user.domain'].isin({d.lower() for d in domain})     
            
        # all the entries for the specified user
        df1 = dataframe[(~dataframe['group.id'].isnull()) & (filter2)]
        
        # all the groups associated to the user
        group_ids = df1['group.id'].unique()
        
        # all the entries for the associated groups (related to a LP, not a Fund or a Vehicle), whatever the user
        df2 = dataframe[(~dataframe['intralinks_user.emailId'].isnull()) & (dataframe['group.id'].isin(group_ids)) & (dataframe['group.list_type'] == 'LP')]
        df3 = df2.pivot_table(index=[
            'exchange.id', 
            'exchange.workspaceName', 
            'group.id', 
            'group.groupName', 
            'group.list_type', 
            'group.list_id', 
            'group.doc_type'
        ], columns='user.emailId', aggfunc={'group.id':len})
        
        return df3.fillna('')

    def get_memberships(self, user):
        email = user if isinstance(user, str) else user['emailId']

        df = self.dataframe[self.dataframe['intralinks_user.emailId'].astype(str).str.lower() == email.lower()]
        df = df.fillna('')
        df = df.sort_values(['exchange.workspaceName', 'group.groupName'])
        df = df.reset_index()
        df = df[['exchange.id', 'exchange.workspaceName', 'exchange_member.roleType', 'group.groupName']]
        df = df.drop_duplicates()
        df.columns = ['Exchange ID', 'Exchange Name', 'Role', 'Group']

        return df
    
    def copy_memberships(self, from_user, to_user):
        from_email = from_user if isinstance(from_user, str) else from_user['emailId']

        if isinstance(to_user, str):
            to_user = self.il.get_user_account(to_user, exchange_id=None)

        elif isinstance(to_user, tuple):
            to_user = entity_to_dict(to_user)
        
        df = self.dataframe[self.dataframe['intralinks_user.emailId'].astype(str).str.lower() == from_email.lower()]
        df = df.fillna('')
        df = df.sort_values(['exchange.workspaceName', 'group.groupName'])
        df = df.reset_index()
        df = df[['exchange.id', 'exchange.workspaceName', 'exchange_member.roleType', 'group.groupName']]
        df = df.drop_duplicates()
        df.columns = ['Exchange ID', 'Exchange Name', 'Role', 'Group']
        df['First Name'] = to_user['firstName']
        df['Last Name'] = to_user['lastName']
        df['Email'] = to_user['emailId']
        df['Organization'] = to_user['organization']
        df['Phone'] = '0000'
        df = df[['First Name', 'Last Name', 'Email', 'Phone', 'Organization', 'Exchange ID', 'Exchange Name', 'Role', 'Group']]

        file_name = 'data/{}_{}.xlsx'.format(to_user['emailId'], datetime.datetime.today().strftime('%Y%m%d_%H%M%S'))
        df.to_excel(file_name, index=False)

        print('Saved to {}'.format(file_name))

        return df
    
class UserManagerUI:
    def __init__(self, user_manager, login_manager):
        self.user_manager = user_manager
        self.login_manager_ui = intralinks.tools.login_manager.LoginManagerUI(login_manager)
        self.wm = intralinks.tools.notebooks_goodies.WidgetManager()

        def log(self, operation, count=None, step=None, wm=self.wm, style=None):
            if operation == 'load_users_and_groups_from_intralinks':
                if count is not None:
                    wm['scope_load_il.progress'].max = count
                    wm['scope_load_il.progress'].value = 0

                if step is not None:
                    wm['scope_load_il.progress'].value += 1
                    wm['scope_load_il.status'].value = 'Loading {} - {}'.format(step['id'], step['workspaceName'])

                if style is not None:
                    wm['scope_load_il.progress'].bar_style = style
        
        setattr(self.user_manager, 'log', log.__get__(self.user_manager, self.user_manager.__class__))
        
    def action_load_file(self, f, s):
        try:
            self.wm[s].value = 'Loading file...'
            file = self.wm[f].value

            self.user_manager.load_from_file(file)
            self.user_manager.categorize_data()
            self.user_manager.prepare_dataframe()

            self.wm[s].value = 'File loaded!'
        except:
            self.wm[s].value = 'Error, see below!'
            raise

    def action_load_intralinks(self, r, e, s):
        report = self.wm[r].value
        exchanges = [int(i) for i in re.split('[,; ]\s*', self.wm[e].value)]
        
        try:
            self.wm[s].value = 'Loading from Intralinks...'
            
            if report == 'All exchanges':
                self.user_manager.load_exchanges_from_intralinks()

            elif report == 'All exchanges where MANAGER':
                self.user_manager.load_exchanges_from_intralinks(is_manager=True)

            elif report == 'All exchanges except <scope>':
                self.user_manager.load_exchanges_from_intralinks()
                self.user_manager.exchanges = [e for e in self.user_manager.exchanges if int(e['id']) not in exchanges]
                
            elif report == 'Only exchanges <scope>':
                self.user_manager.load_exchanges_from_intralinks()
                self.user_manager.exchanges = [e for e in self.user_manager.exchanges if int(e['id']) in exchanges]
            
            self.user_manager.load_users_and_groups_from_intralinks()
            self.user_manager.categorize_data()
            self.user_manager.prepare_dataframe()

            self.wm[s].value = 'Data loaded!'
        except:
            self.wm[s].value = 'Error, see below!'
            raise

    def action_find_user(self, e, r):
        email = self.wm[e].value
        exchange = self.wm[r].value

        u = self.user_manager.il.get_user_account(email, exchange=exchange)

        print(u)
        
    def action_report_user(self, e, r, s):
        email = self.wm[e].value
        report = self.wm[r].value
        
        if report == 'Exchanges':
            create_code_cell("""user_manager.exchanges_for(user='{}')""".format(email))
            self.wm[s].value = 'Please execute the instruction below!'
        
        elif report == 'Exchanges & Groups':
            create_code_cell("""user_manager.get_memberships(email='{}')""".format(email))
            self.wm[s].value = 'Please execute the instruction below!'
        
        else:
            self.wm[s].value = 'Error: Unknown Choice'

    def action_report_team(self, i, r, s):
        teamid = self.wm[i].value.strip()
        report = self.wm[r].value
        
        is_email = False
        is_domain = False
        
        if '@' in teamid:
            if teamid.startswith('@'):
                is_domain = True
                teamid = teamid[1:] 
                
            else:
                is_email = True
        
        if report == 'Exchanges':
            create_code_cell("""df = user_manager.exchanges_for(email='{}')\n#df.to_excel('exchanges.xlsx')\ndf""".format(teamid))
            self.wm[s].value = 'Please execute the instruction below!'
        
        elif report == 'Exchanges & Groups':
            if is_email:
                create_code_cell("""df = user_manager.team_for(email='{}')\n#df.to_excel('team.xlsx')\ndf""".format(teamid))
                self.wm[s].value = 'Please execute the instruction below!'
            elif is_domain:
                create_code_cell("""df = user_manager.team_for(domain='{}')\n#df.to_excel('team.xlsx')\ndf""".format(teamid))
                self.wm[s].value = 'Please execute the instruction below!'
        
        else:
            self.wm[s].value = 'Error: Unknown Choice'

    def action_report_other(self, r, s):
        report = self.wm[r].value
        
        if report == 'Top Users':
            create_code_cell("""user_manager.top_users()""")
            self.wm[s].value = 'Please execute the instruction below!'
        
        elif report == 'Top Groups':
            create_code_cell("""user_manager.top_groups()""")
            self.wm[s].value = 'Please execute the instruction below!'

        elif report == 'Top Investors':
            create_code_cell("""user_manager.top_investors()""")
            self.wm[s].value = 'Please execute the instruction below!'      
            
        elif report == 'Orphan Users':
            create_code_cell("""user_manager.orphans()""")
            self.wm[s].value = 'Please execute the instruction below!'    
        
        else:
            self.wm[s].value = 'Error: Unknown Choice'
        
    def loader_panel(self):
        self.wm.register_widget(self.login_manager_ui.login_panel(), key='login.panel', description='Login')

        self.wm.RadioButtons(options=[
            'All exchanges where MANAGER', 
            'All exchanges', 
            'All exchanges except <scope>', 
            'Only exchanges <scope>'
        ], key='scope_load_il.type')
        self.wm.Text(description='Scope', key='scope_load_il.value', value='5861355, 5861365, 5861375, 5861385')
        self.wm.Button(description='Load', action=lambda d:self.action_load_intralinks('scope_load_il.type', 'scope_load_il.value', 'scope_load_il.status'), key='scope_load_il.button')
        self.wm.IntProgress(key='scope_load_il.progress')
        self.wm.Label(key='scope_load_il.status')

        self.wm.VBox('scope_load_il.type|scope_load_il.value|scope_load_il.button|scope_load_il.progress|scope_load_il.status', key='scope_load_il.panel', description='Scope')

        self.wm.Text(description='File', key='load_file.file', value='data/users/_data.json')
        self.wm.Button(description='Load', action=lambda d:self.action_load_file('load_file.file', 'load_file.status') , key='load_file.button')
        self.wm.Label(key='load_file.status')

        self.wm.VBox('load_file.file|load_file.button|load_file.status', key='load_file.panel', description='Load from file')

        self.wm.Accordion('login.panel|scope_load_il.panel', key='load_il.panel', description='Load from Intralinks')

        return self.wm.Tab('load_il.panel|load_file.panel')

    def analytics_panel(self):
        # User Details

        self.wm.Text(description='Email', key='find_user.email', value='hdegabrielli@intralinks.com')
        self.wm.Text(description='Exchange', key='find_user.exchange', value='2092305')
        self.wm.Button(description='Find', key='find_user.button', action=lambda b:self.action_find_user('find_user.email', 'find_user.exchange'))
        self.wm.Label(key='find_user.status')
        
        self.wm.VBox('find_user.email|find_user.exchange|find_user.button|find_user.status', key='find_user.panel', description='Find User')

        # User Access Rights

        self.wm.Text(description='Email', value='helene.falchier@cnp.fr', key='user_report.email')
        self.wm.RadioButtons(description='Report Type', options=[
            'Exchanges', 
            'Exchanges & Groups'
        ], key='user_report.report')
        self.wm.Button(description='Show', action=lambda b:self.action_report_user('user_report.email', 'user_report.report', 'user_report.status'), key='user_report.button')
        self.wm.Label(key='user_report.status')

        self.wm.VBox('user_report.email|user_report.report|user_report.button|user_report.status', key='user_access.panel', description='User Access')

        # Team Access Rights

        self.wm.Text(description='Email or domain or team', key='group_report.id')
        self.wm.RadioButtons(description='Report Type', options=[
            'Exchanges', 
            'Exchanges & Groups'
        ], key='group_report.report')
        self.wm.Button(description='Show', action=lambda b:self.action_report_team('group_report.id', 'group_report.report', 'group_report.status'),  key='group_report.button')
        self.wm.Label(key='group_report.status')

        self.wm.VBox('group_report.id|group_report.report|group_report.button|group_report.status', key='team_access.panel', description='Team Access')

        # Other Reports

        self.wm.RadioButtons(description='Report Type', options=[
            'Top Users', 
            'Top Groups',
            'Top Investors',
            'Orphan Users',
        ], key='other_report.report')
        self.wm.Button(description='Show', action=lambda b:self.action_report_other('other_report.report', 'other_report.status'),  key='other_report.button')
        self.wm.Label(key='other_report.status')

        self.wm.VBox('other_report.report|other_report.button|other_report.status', key='other_report.panel', description='Other reports')

        return self.wm.Tab('find_user.panel|user_access.panel|team_access.panel|other_report.panel')

    def main_panel(self):
        return ipywidgets.widgets.VBox([
            self.loader_panel(), 
            self.analytics_panel()
        ])
