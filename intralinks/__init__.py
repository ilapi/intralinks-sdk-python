
"""
For educational purpose only
"""

import intralinks.api
import intralinks.api.v2

import intralinks.utils.http

import intralinks.authenticators.v1.authentication
import intralinks.authenticators.v2.authentication

from intralinks.utils.data import entity_to_dict

import intralinks.functions.v1.exchanges
import intralinks.functions.v1.splashes
import intralinks.functions.v1.folders
import intralinks.functions.v1.documents
import intralinks.functions.v1.groups
import intralinks.functions.v1.exchange_members
import intralinks.functions.v1.batches
import intralinks.functions.v1.permissions
import intralinks.functions.v1.custom_alerts
import intralinks.functions.v1.fields
import intralinks.functions.v1.user_accounts

import intralinks.functions.v2.exchanges
import intralinks.functions.v2.splashes
import intralinks.functions.v2.folders
import intralinks.functions.v2.documents
import intralinks.functions.v2.groups
import intralinks.functions.v2.exchange_members
import intralinks.functions.v2.batches
import intralinks.functions.v2.permissions
import intralinks.functions.v2.fields
import intralinks.functions.v2.user_accounts

class IntralinksClient:
    def __init__(self, api_client=None, use_v1=False, max_retry=2):        
        self.api_client = api_client
        self.use_v1 = use_v1
        self.max_retry = max_retry

    def diagnose(self):
        response = self.api_client.last_response
        try:
            get_ipython
            intralinks.utils.http.display_last_response(response)
        except:
            intralinks.utils.http.print_last_response(response)

    def _update_param(self, entity, result, update_param=True):
        if update_param:
            if isinstance(entity, tuple):
                entity = entity_to_dict(entity)

            entity.update(result)
            return entity
        else:
            return result

    def _update_param_as_list(self, entities, result, update_param=True):
        if update_param:
            for e, r in zip(entities, result):
                e.update(r)
            return entities
        else:
            return result
    
    def _get_id(self, entity, key='id'):
        if entity is None:
            return None
        elif isinstance(entity, int) or isinstance(entity, str):
            return entity
        else:
            return entity[key]
    
    def _retry(self, call):
        exception = None

        for count in range(0, self.max_retry):
            try:
                return call()

            except intralinks.api.ApiException as e:
                if e.message.startswith('JavaScript execution failed: Unterminated string literal'):
                    print('... Retrying')
                    exception = e
                else:
                    raise e

            except ConnectionError as e:
                exception = e

        raise exception

    ###########################################################################################################
    # Authentication
    ###########################################################################################################

    def build_oauth_url(self, state, end_other_sessions=False):
        if self.api_client.is_v1():
            raise Exception()
        else:
            return intralinks.authenticators.v2.authentication.build_oauth_url(self.api_client, state, end_other_sessions)

    def validate_oauth_code(self, code):
        if self.api_client.is_v1():
            raise Exception()
        else:
            return intralinks.authenticators.v2.authentication.validate_oauth_code(self.api_client, code)

    def login(self, email, password, end_other_sessions=False, secure_id_callback=None):
        if self.api_client.is_v1():
            try:
                intralinks.authenticators.v1.authentication.login(self.api_client, email, password)
            except intralinks.authenticators.v1.authentication.AlreadyLoggedInException as e:
                if end_other_sessions:
                    intralinks.authenticators.v1.authentication.special_login(self.api_client, self.api_client.session.email, self.api_client.session.password, secure_id=None, end_other_sessions=True)
                else:
                    raise e1
            except intralinks.authenticators.v1.authentication.SecureIdRequiredException as e:
                if secure_id_callback:
                    secure_id = secure_id_callback()
                    intralinks.authenticators.v1.authentication.special_login(self.api_client, self.api_client.session.email, self.api_client.session.password, secure_id=secure_id, end_other_sessions=end_other_sessions)

            intralinks.authenticators.v1.authentication.get_flags(self.api_client)
        else:
            intralinks.authenticators.v2.authentication.login(self.api_client, email, password, end_other_sessions)
    
    def logout(self):
        if self.api_client.is_v1():
            return intralinks.authenticators.v1.authentication.logout(self.api_client)
        else:
            return intralinks.authenticators.v2.authentication.logout(self.api_client)

    ###########################################################################################################
    # User Accounts
    ###########################################################################################################

    def get_user_account(self, email, exchange=None):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.user_accounts.get_user_account(self.api_client, email, exchange_id)
        else:
            return self._retry(lambda: intralinks.functions.v2.user_accounts.get_user_account(self.api_client, email, exchange_id))

    def create_user_account(self, email, first_name, last_name, organization, phone, language):
        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.user_accounts.create_user_account(self.api_client, email, first_name, last_name, organization, phone, language)
        else:
            return intralinks.functions.v2.user_accounts.create_user_account(self.api_client, email, first_name, last_name, organization, phone, language)

    ###########################################################################################################
    # Exchanges
    ###########################################################################################################

    def get_exchanges(self, user=None, is_manager=None):
        user_id = self._get_id(user, 'userId')

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.exchanges.get_exchanges(self.api_client, user_id=user_id, is_manager=is_manager)
        else:
            return self._retry(lambda: intralinks.functions.v2.exchanges.get_exchanges(self.api_client, user_id=user_id, is_manager=is_manager))

    def get_exchange(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.exchanges.get_exchange(self.api_client, exchange_id)
        else:
            return self._retry(lambda: intralinks.functions.v2.exchanges.get_exchange(self.api_client, exchange_id))
    
    def get_exchange_settings(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.exchanges.get_exchange_settings(self.api_client, exchange_id)
        else:
            raise Exception()

    def create_exchange(self, exchange, suppress_welcome_alert=True, update_param=True):
        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.exchanges.create_exchange(self.api_client, exchange, suppress_welcome_alert)
        else:
            result = intralinks.functions.v2.exchanges.create_exchange(self.api_client, exchange, suppress_welcome_alert)

        if update_param:
            exchange = entity_to_dict(exchange)
            exchange.update(result)
            exchange['id'] = exchange.pop('workspaceId')

            return exchange
        else:
            return result
    
    def update_exchange(self, exchange, is_phase_updated=False):
        if self.api_client.is_v1() or self.use_v1:
            intralinks.functions.v1.exchanges.update_exchange(self.api_client, exchange, is_phase_updated)
        else:
            intralinks.functions.v2.exchanges.update_exchange(self.api_client, exchange, is_phase_updated)
        
        return exchange
    
    ###########################################################################################################
    # Splash
    ###########################################################################################################

    def get_splash(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.splashes.get_splash(self.api_client, exchange_id)
        else:
            return self._retry(lambda: intralinks.functions.v2.splashes.get_splash(self.api_client, exchange_id))
    
    def download_splash_image(self, exchange, path_without_extension):
        exchange_id = self._get_id(exchange)

        return intralinks.functions.v1.splashes.download_splash_image(self.api_client, exchange_id, path_without_extension)
    
    def enter_exchange(self, exchange, accept_splash=None):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.splashes.enter_exchange(self.api_client, exchange_id, accept_splash=accept_splash)
        else:
            return intralinks.functions.v2.splashes.enter_exchange(self.api_client, exchange_id, accept_splash=accept_splash)
    
    ###########################################################################################################
    # Folders
    ###########################################################################################################

    def get_folders(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.folders.get_folders(self.api_client, exchange_id)  
        else:  
            return self._retry(lambda: intralinks.functions.v2.folders.get_folders(self.api_client, exchange_id))
    
    def create_folder(self, exchange, folder, update_param=True):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.folders.create_folder(self.api_client, exchange_id, folder)
        else:
            result = intralinks.functions.v2.folders.create_folder(self.api_client, exchange_id, folder)

        return self._update_param(folder, result, update_param)

    def create_folders(self, exchange, folders, update_param=True):
        exchange_id = self._get_id(exchange)

        result = None

        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.folders.create_folders(self.api_client, exchange_id, folders)
        else:
            raise Exception()
        
        self._update_param_as_list(folders, result, update_param)

    def update_folder(self, exchange, folder, update_param=True):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.folders.update_folder(self.api_client, exchange_id, folder)
        else:
            result = intralinks.functions.v2.folders.update_folder(self.api_client, exchange_id, folder)
        
        return self._update_param(folder, result, update_param) 

    def delete_folder(self, exchange, folder):
        exchange_id = self._get_id(exchange)
        id = folder['id']
        version = folder['version']

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.folders.delete_folder(self.api_client, exchange_id, id, version)
        else:
            return intralinks.functions.v2.folders.delete_folder(self.api_client, exchange_id, id, version)

    def delete_folders(self, exchange, folders):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.folders.delete_folders(self.api_client, exchange_id, folders)
        else:
            return intralinks.functions.v2.folders.delete_folders(self.api_client, exchange_id, folders)

    ###########################################################################################################
    # Documents & Files
    ###########################################################################################################

    def get_documents(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.documents.get_documents(self.api_client, exchange_id)
        else:
            return self._retry(lambda: intralinks.functions.v2.documents.get_documents(self.api_client, exchange_id))
        
    def create_document(self, exchange, document, file=None, batch_id=None, update_param=True):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.documents.create_document(self.api_client, exchange_id, document, file=file, batch_id=batch_id)
        else:
            result = intralinks.functions.v2.documents.create_document(self.api_client, exchange_id, document)
        
        return self._update_param(document, result, update_param)

    def create_documents(self, exchange, documents, batch_id=None):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.documents.create_document(self.api_client, exchange_id, documents, batch_id)
        else:
            raise Exception()

    def download_file(self, exchange, document, file_path):
        exchange_id = self._get_id(exchange)
        document_id = self._get_id(document)

        if self.api_client.is_v1() or self.use_v1:
            raise Exception()
        else:
            return intralinks.functions.v2.documents.download_file(self.api_client, exchange_id, document_id, file_path)

    def upload_file(self, exchange, document, version, file_path):
        exchange_id = self._get_id(exchange)
        document_id = self._get_id(document)

        if self.api_client.is_v1() or self.use_v1:
            raise Exception()
        else:
            return intralinks.functions.v2.documents.upload_file(self.api_client, exchange_id, document_id, version, file_path)

    def update_document(self, exchange, document, update_param=True):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.documents.update_document(self.api_client, exchange_id, document)
        else:
            result = intralinks.functions.v2.documents.update_document(self.api_client, exchange_id, document)
        
        return self._update_param(document, result, update_param)

    def delete_document(self, exchange, document):
        exchange_id = self._get_id(exchange)
        id = document['id']
        version = document['version']

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.documents.delete_document(self.api_client, exchange_id, id, version)
        else:
            return intralinks.functions.v2.documents.delete_document(self.api_client, exchange_id, id, version)

    def delete_documents(self, exchange, documents):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.documents.delete_documents(self.api_client, exchange_id, documents)
        else:
            return intralinks.functions.v2.documents.delete_documents(self.api_client, exchange_id, documents)
    
    ###########################################################################################################
    # Exchange Members
    ###########################################################################################################

    def get_exchange_members(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.exchange_members.get_exchange_members(self.api_client, exchange_id)
        else:
            return self._retry(lambda: intralinks.functions.v2.exchange_members.get_exchange_members(self.api_client, exchange_id))

    def get_removed_exchange_members(self, exchange):
        exchange_id = self._get_id(exchange)

        return intralinks.functions.v1.exchange_members.get_removed_exchange_members(self.api_client, exchange_id)

    def create_exchange_member(self, exchange, exchange_member, alert=None, update_param=True):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.exchange_members.create_exchange_member(self.api_client, exchange_id, exchange_member)
        else:
            result = intralinks.functions.v2.exchange_members.create_exchange_member(self.api_client, exchange_id, exchange_member, alert)
        
        if update_param:
            if isinstance(exchange_member, tuple):
                exchange_member = entity_to_dict(exchange_member)
            
            user = exchange_member.pop('user')

            if isinstance(user, tuple):
                user = entity_to_dict(user)
            
            exchange_member.update(user)

            exchange_member['emailId'] = result.pop('email')
            exchange_member.update(result)

            return exchange_member
        else:
            return result

    def update_exchange_member(self, exchange, exchange_member, update_param=True):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.exchange_members.update_exchange_member(self.api_client, exchange_id, exchange_member)
        else:
            result = intralinks.functions.v2.exchange_members.update_exchange_member(self.api_client, exchange_id, exchange_member)
        
        return self._update_param(exchange_member, result, update_param)

    def delete_exchange_member(self, exchange, exchange_member):
        exchange_id = self._get_id(exchange)
        id = exchange_member['id']
        version = exchange_member['version']

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.exchange_members.delete_exchange_member(self.api_client, exchange_id, id, version)
        else:
            return intralinks.functions.v2.exchange_members.delete_exchange_member(self.api_client, exchange_id, id, version)

    def delete_exchange_members(self, exchange, exchange_members):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.exchange_members.delete_exchange_members(self.api_client, exchange_id, exchange_members)
        else:
            raise Exception()

    ###########################################################################################################
    # Groups
    ###########################################################################################################

    def get_groups(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.groups.get_groups(self.api_client, exchange_id)
        else:
            return self._retry(lambda: intralinks.functions.v2.groups.get_groups(self.api_client, exchange_id))
    
    def get_groups_and_members(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.groups.get_groups_and_members(self.api_client, exchange_id)
        else:
            return self._retry(lambda: intralinks.functions.v2.groups.get_groups_and_members(self.api_client, exchange_id))
    
    def create_group(self, exchange, group, update_param=True):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.groups.create_group(self.api_client, exchange_id, group)
        else:
            result = intralinks.functions.v2.groups.create_group(self.api_client, exchange_id, group)
        
        return self._update_param(group, result, update_param)

    def update_group(self, exchange, group, remove_group_members=None, add_group_members=None, update_param=True):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            result = intralinks.functions.v1.groups.update_group(self.api_client, exchange_id, group, remove_group_members=remove_group_members, add_group_members=add_group_members)
        else:
            result = intralinks.functions.v2.groups.update_group(self.api_client, exchange_id, group, remove_group_members=remove_group_members, add_group_members=add_group_members)
        
        return self._update_param(group, result, update_param) 

    def delete_group(self, exchange, group, remove_users=False):
        exchange_id = self._get_id(exchange)
        id = group['id']
        version = group['version']

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.groups.delete_group(self.api_client, exchange_id, id, version, remove_users)
        else:
            return intralinks.functions.v2.groups.delete_group(self.api_client, exchange_id, id, version, remove_users)

    def delete_groups(self, exchange, groups, remove_users=False):
        exchange_id = self._get_id(exchange)

        results = []

        for group_sublist in intralinks.utils.data.chunks(groups, intralinks.functions.validations.GROUP_MAX_ENTITY_COUNT_DELETE):
            if self.api_client.is_v1() or self.use_v1:
                result = intralinks.functions.v1.groups.delete_groups(self.api_client, exchange_id, group_sublist, remove_users)
            else:
                result = intralinks.functions.v2.groups.delete_groups(self.api_client, exchange_id, group_sublist, remove_users)
            
            results.append(result)
        
        return results

    ###########################################################################################################
    # Group Members
    ###########################################################################################################

    def add_member_to_group(self, exchange, group, exchange_member):
        exchange_id = self._get_id(exchange)
        group_id = self._get_id(group)
        exchange_member_id = self._get_id(exchange_member)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.groups.add_member_to_group(self.api_client, exchange_id, group_id, exchange_member_id)
        else:
            return intralinks.functions.v2.groups.create_group_member(self.api_client, exchange_id, group_id, exchange_member_id)
    
    def add_member_from_group(self, exchange, group, exchange_member):
        exchange_id = self._get_id(exchange)
        group_id = self._get_id(group)
        exchange_member_id = self._get_id(exchange_member)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.groups.remove_member_from_group(self.api_client, exchange_id, group_id, exchange_member_id)
        else:
            return intralinks.functions.v2.groups.create_group_member(self.api_client, exchange_id, group_id, exchange_member_id)


    ###########################################################################################################
    # Bulk Upload
    ###########################################################################################################

    def get_bulk_uploads(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            raise Exception()
        else:
            return self._retry(lambda: intralinks.functions.v2.batches.get_batches(self.api_client, exchange_id, operation_type='Bulk Upload'))
    
    def get_bulk_upload_items(self, exchange, bulk_upload_id):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            raise Exception()
        else:
            return self._retry(lambda: intralinks.functions.v2.batches.get_batch_items(self.api_client, exchange_id, bulk_upload_id))
    
    def get_permissions(self, exchange, document):
        exchange_id = self._get_id(exchange)
        document_id = self._get_id(document)

        if self.api_client.is_v1() or self.use_v1:
            raise Exception()
        else:
            return self._retry(lambda: intralinks.functions.v2.permissions.get_permissions(self.api_client, exchange_id, document_id))
    
    def get_access_statuses(self, exchange, document):
        exchange_id = self._get_id(exchange)
        document_id = self._get_id(document)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.documents.get_access_statuses(self.api_client, exchange_id, document_id)
        else:
            return self._retry(lambda: intralinks.functions.v2.documents.get_access_statuses(self.api_client, exchange_id, document_id))
    
    def get_custom_alerts(self, resource_type, resource_id, alert_type, alert_locale=None):
        return intralinks.functions.v1.custom_alerts.get_custom_alerts(self.api_client, resource_type, resource_id, alert_type, alert_locale)
    
    def get_field_definitions(self, exchange):
        exchange_id = self._get_id(exchange)

        if self.api_client.is_v1() or self.use_v1:
            return intralinks.functions.v1.fields.get_field_definitions(self.api_client, exchange_id)
        else:
            return self._retry(lambda: intralinks.functions.v2.fields.get_field_definitions(self.api_client, exchange_id))

def new_client(base_url, session_token=None):
    config = intralinks.api.v2.Config(
        base_url
    )

    session = intralinks.api.v2.Session(
        session_token
    )

    api_client = intralinks.api.ApiClient(config, session)

    return intralinks.IntralinksClient(api_client)
