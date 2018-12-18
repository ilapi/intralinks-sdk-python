import collections

class ExchangePhase:
    OPEN = 'OPEN'
    PREPARATION = 'PREPARATION'
    HOLD = 'HOLD'

class GroupType:
    EXCHANGE_GROUP = 'WORKSPACE'
    BUYER_GROUP = 'BUYER' 
    COLLABORATION_GROUP = 'COLLABORATION'

class Permission:
    SEE = 'SEE'
    CONTROL = 'CONTROL'
    REVOKED = 'REVOKED'

class IRM:
    NONE = 'NONE'
    NOSAVE = 'NOSAVE'
    NOSAVENOPRINT = 'NOSAVENOPRINT'

class AlertDetailsType:
    WELCOME_NEW_USER = 'WELCOME_NEW_USER'
    WELCOME_EXISTING_USER = 'WELCOME_EXISTING_USER'

    NEW_DOCUMENT = 'NEW_DOCUMENT_ALERT'
    MULTI_DOCUMENT = 'MULTI_DOCUMENT_ALERT'
    BULK_DOCUMENT = 'BULK_DOCUMENT_ALERT'
    UPDATED_DOCUMENT = 'UPDATED_DOCUMENT_ALERT'

    NEW_UPDATE_PUBLICATION_COMMENT = 'NEW_UPDATE_PUBLICATION_COMMENT'

class AlertResourceType:
    EXCHANGE = 9
    TEMPLATE = 8

class AlertType:
    NEW_DOCUMENT_SINGLE = 0
    NEW_DOCUMENT_BULK = 2
    NEW_DOCUMENT_MULTIFILE = 145
    WELCOME_USER_NEW = 113
    WELCOME_USER_EXISTING = 109

def namedtuple(name, field_names, defaults):
    entity_class = collections.namedtuple(name, field_names)
    entity_class.__new__.__defaults__ = tuple(defaults)
    return entity_class

_EntityField = namedtuple('EntityField', ('name', 'default', 'mandatory'), defaults=(None, False))

user_account_fields = [
    _EntityField('emailId', mandatory=True), 
    _EntityField('firstName', mandatory=True), 
    _EntityField('lastName', mandatory=True),
    _EntityField('organization', mandatory=True),
    _EntityField('officePhone', default='0000'), 
    _EntityField('languagePref', default='en_US')
]

UserAccount = namedtuple(
    'UserAccount', 
    field_names=(f.name for f in user_account_fields), 
    defaults=(f.default for f in user_account_fields if not f.mandatory)
) 

exchange_fields = [
    _EntityField('workspaceName', mandatory=True), 
    _EntityField('hostName', mandatory=True), 
    _EntityField('templateId', mandatory=True),
    _EntityField('phase', default=ExchangePhase.OPEN),
    _EntityField('description', default=None)
]

Exchange = namedtuple(
    'Exchange', 
    field_names=(f.name for f in exchange_fields), 
    defaults=(f.default for f in exchange_fields if not f.mandatory)
)  

document_fields = [
    _EntityField('name', mandatory=True),
    _EntityField('parentId', mandatory=True),
    _EntityField('note', default=None),
    _EntityField('noteRequired', default=None),
    _EntityField('urlNote', default=None),
    _EntityField('effectiveDate', default=None),
]

Document = namedtuple(
    'Document', 
    field_names=(f.name for f in document_fields), 
    defaults=(f.default for f in document_fields if not f.mandatory)
)

folder_fields = [
    _EntityField('name', mandatory=True),
    _EntityField('parentId', default=None),
    _EntityField('note', default=None),
    _EntityField('indexingDisabled', default=False)
]

Folder = namedtuple(
    'Folder', 
    field_names=(f.name for f in folder_fields), 
    defaults=(f.default for f in folder_fields if not f.mandatory)
)

group_fields = [
    _EntityField('groupName', mandatory=True),
    _EntityField('groupType', default=GroupType.EXCHANGE_GROUP),
    _EntityField('note', default=None),
    _EntityField('ftsEnabled', default=False),
    _EntityField('defaultFolderPath', default=None)
]

Group = namedtuple(
    'Group', 
    field_names=(f.name for f in group_fields), 
    defaults=(f.default for f in group_fields if not f.mandatory)
)

exchange_member_fields = [
    _EntityField('user', mandatory=True),
    _EntityField('roleType', mandatory=True),
    _EntityField('keyContact', default=False),
    _EntityField('unauthenticatedDocumentAccess', default=False),
    _EntityField('qnaAttributes', default=None),
]

ExchangeMember = namedtuple(
    'ExchangeMember', 
    field_names=(f.name for f in exchange_member_fields), 
    defaults=(f.default for f in exchange_member_fields if not f.mandatory)
)

alert_fields = [
    _EntityField('customNote', mandatory=True),
    _EntityField('customSubject', mandatory=True)
]

Alert = namedtuple(
    'Alert', 
    field_names=(f.name for f in alert_fields), 
    defaults=(f.default for f in alert_fields if not f.mandatory)
)

VersionedEntity = collections.namedtuple('VersionedEntity', 'id version')

def new_permission(group, permission, irm=IRM.NONE):
    return strip_dict({
        'granteeInfo': {
            'granteeId':group['id'], 
            'granteeType':'WORKSPACE', 
            'isWorkspaceUser': False
        },
        'isInherited':False,
        'permission':permission,
        'drm':irm
    })
