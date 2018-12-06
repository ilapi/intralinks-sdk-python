import xml.sax
import xml.sax.saxutils
import intralinks.utils.data

def to_xml_value(v):
    if isinstance(v, dict) or isinstance(v, list):
        return to_xml(v)
    else:
        if isinstance(v, bool):
            v = 'T' if v else 'F'
        else:
            v = str(v)
        
        return xml.sax.saxutils.escape(v)

def to_xml_entity(d):
    return ['<{}>{}</{}>'.format(k, to_xml_value(d[k]), k) for k in d if d[k] is not None]

def to_xml(d, tag = None):
    tag = intralinks.utils.data.as_list(tag)

    if isinstance(d, dict):
        l = to_xml_entity(d)

    elif isinstance(d, list):
        l = []

        for e in d:
            if tag:
                l.append('<{}>'.format(tag[0]))

            l.extend(to_xml_entity(e))

            if tag:
                l.append('</{}>'.format(tag[0]))

        if tag:
            tag = tag[1:]
    
    if tag is not None:
        l = ['<{}>'.format(t) for t in reversed(tag)] + l + ['</{}>'.format(t) for t in tag]

    return ''.join(l)

class IntralinksNode():
    def __init__(self):
        self.full_path = None
        self.name = None
        self.value = None
        self.children = None
        self.content = None

number_tags = {
    'id', 
    'workspaceId',
    'parentTemplateId',
    'parentId',
    'sharedResourceId',
    'userId', 
    'workspaceGroupId', 
    'workspaceUserId',
    'organizationId',
    'code',  
    'securityLevel', 
    'milliseconds', 
    'lastLoginDate',
    'fileSize',  
    'pageCount', 
    'orderNumber', 
    'versionNumber', 
    'groupMemberCount',
    'sharedResourceCount',  
    'newParticipantRequests', 
    'newTasks', 
    'highPriorityQuestionSubmitted', 
    'lowPriorityQuestionSubmitted', 
    'mediumPriorityQuestionSubmitted'
}

boolean_tags = {
    'global', 
    'htmlViewEnabled', 
    'pvpEnabled', 
    'hasImage', 
    'splashRequired', 
    'hasNote', 
    'isBusinessProcessEnabled', 
    'isDeleted', 
    'isFavorite', 
    'isIrmSecured', 
    'noteRequired', 
    'unread', 
    'hasChildFolders', 
    'indexingDisabled', 
    'isEmailin', 
    'doNotSendAlert', 
    'isPlaceholderUser', 
    'isWelcomeAlertSent', 
    'keyContact', 
    'buyerAttachFilesAllowed', 
    'discussionAllowed', 
    'submitterAttachFilesAllowed', 
    'ftsEnabled',
    'canSet',
    'readOnly',
    'isActive',
    'isHidden',
    'required',
    'workflowEnabled',
    'isWorkspaceUser',
    'implicitPermission',
    'isInherited',
    'seeOnly',
    'isAdminUser',
    'isLinkedUp'
}

class IntralinksHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.path = None
        self.children = []
        
    def startDocument(self):
        self.path = []
        
    def startElement(self, name, attrs):
        node = IntralinksNode()
        self.path.append(node)
        node.name = name
        node.full_path = [n.name for n in self.path]
        node.full_path_name = '/'.join(node.full_path)
        
        if len(self.path) > 1:
            parent = self.path[-2]
            
            if parent.children is None:
                parent.children = []
                
            parent.children.append(node)
    
    def characters(self, content):
        current_node = self.path[-1]
        
        if current_node.content is None:
            current_node.content = []
            
        current_node.content.append(content)
    
    def as_object_or_list(self, o, path):
        path_name = '/'.join(path)
        
        if path_name.endswith('/errors/error') or path_name.endswith('/workspaceResponse/workspace') or path_name.endswith('/folderListResponse/folder'):
            return [o]
        else:
            return {path[-1]:o}
    
    def endElement(self, name):
        current_node = self.path.pop()
        
        if current_node.name != name:
            print('Error at endElement: current_node.name != name')
        
        if current_node.content is not None and current_node.children is not None:
            print('Error at endElement: current_node.content is not None and current_node.children is not None')
            
        elif current_node.content is not None:
            value = ''.join(current_node.content)
            
            if current_node.name in number_tags:
                value = int(value)
            
            elif current_node.name in boolean_tags:
                if value not in {'F', 'T', 'false', 'true'}:
                    print('Error at endElement: {} = {} is not a boolean'.format(current_node.name, value))
                    
                value = value in {'T', 'true'}
            
            current_node.value = value
            
        elif current_node.children is not None:
            if len({c.name for c in current_node.children}) != len(current_node.children):
                d = dict()
                
                for c in current_node.children:
                    if c.name not in d:
                        d[c.name] = []
                    d[c.name].append(c.value)
                
                for k in d:
                    if len(d[k]) == 1:
                        d[k] = self.as_object_or_list(d[k][0], current_node.full_path + [k])
                
                current_node.value = d
                
            elif len(current_node.children) > 1:
                current_node.value = {c.name:c.value for c in current_node.children}
                
            else: # maybe a dict or a list
                current_node.value = self.as_object_or_list(current_node.children[0].value, current_node.children[0].full_path)
        
        else:
            #print('Error at endElement: {} has no value'.format(current_node.name))
            pass
        
        current_node.content = None
        current_node.children = None
        
        if len(self.path) == 0:
            self.children.append(current_node)
        
    def endDocument(self):
        if len(self.path) != 0:
            print('Error at endDocument')
    
def from_xml(s):
    handler = IntralinksHandler()
    xml.sax.parseString(s, handler)
    return handler.children[0].value