"""
For educational purpose only
"""

def associate_users_and_groups(users, groups, group_members):
    users_by_id = {u['id']:u for u in users}
    groups_by_id = {g['id']:g for g in groups}
    
    for u in users:
        u['groups'] = []
    
    for g in groups:
        g['groupMembers'] = []
    
    for m in group_members:
        group = groups_by_id[m['workspaceGroupId']]
        user = users_by_id[m['workspaceUserId']]
        
        group['groupMembers'].append(user['id'])
        user['groups'].append(group['id'])
    
    for g in groups:
        if g['groupMemberCount'] != len(g['groupMembers']):
            raise Exception(g)

class PathBuilder:
    def __init__(self, objects):
        self.objects = objects
        self.objects_by_id = {o['id']:o for o in objects}
    
    def get_object(self, object_id):
        return self.objects_by_id[object_id]
    
    def get_parent(self, o):
        return self.get_object(o['parentId'])
    
    def has_parent(self, o):
        return 'parentId' in o and o['parentId'] != -1
    
    def build_paths(self):
        for o in self.objects:
            self.__build_path_helper__(o)
    
    def __build_path_helper__(self, o):
        if 'ids' not in o:
            parent_ids = []
            parent_names = []
            
            if self.has_parent(o):
                parent = self.get_parent(o)
                
                if 'children_ids' not in parent:
                    parent['children_ids'] = []
                    
                parent['children_ids'].append(o['id'])
                
                self.__build_path_helper__(parent)
                parent_ids = parent['ids']
                parent_names = parent['names']
                
            o['ids'] = parent_ids + [o['id']]
            o['names'] = parent_names + [o['name']]
            o['fullPath'] = '/'.join(o['names'])

def build_paths(*arg):
    objects = []
    
    for a in arg:
        objects.extend(a)
    
    PathBuilder(objects).build_paths()

