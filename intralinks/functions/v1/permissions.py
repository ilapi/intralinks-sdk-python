"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list
from intralinks.utils.xml import to_xml

def get_document_permissions(api_client, exchange_id, document_id):
    response = api_client.get(
        '/services/workspaces/permissions', 
        params={
            'workspaceId':exchange_id,
            'documentId':document_id
        },
        api_version=1
    )

    response.check(200, 'text/xml')

    data = response.data()

    return data['permissions']

def get_folder_permissions(api_client, exchange_id, folder_id, include_limited_publisher_permissions=True):
    response = api_client.get(
        '/services/workspaces/permissions/folders', 
        params={
            'workspaceId':exchange_id,
            'folderId':folder_id,
            'includeLPPermissions':include_lp_permissions
        },
        api_version=1
    )

    response.check(200, 'text/xml')

    data = response.data()

    return data['permissions']


"""
<permissionsUpdateRequest>
  <permissionUpdate>
    <entityId>
      <id>12285722438</id>
      <type>DOCUMENT</type>
    </entityId>
    <permissionInfo>
      <granteeInfo>
        <granteeId>11057265</granteeId>
        <granteeType>WORKSPACE</granteeType>
        <isWorkspaceUser>F</isWorkspaceUser>
      </granteeInfo>
      <isInherited>F</isInherited>
      <permission>SEE</permission>
      <drm>NONE</drm>
    </permissionInfo>
    <permissionInfo>
      <granteeInfo>
        <granteeId>37675035</granteeId>
        <granteeType>WORKSPACE</granteeType>
        <isWorkspaceUser>F</isWorkspaceUser>
      </granteeInfo>
      <isInherited>F</isInherited>
      <permission>REVOKED</permission>
      <drm>NONE</drm>
    </permissionInfo>
  </permissionUpdate>
</permissionsUpdateRequest>
"""

def update_document_permissions(api_client, exchange_id, document_id, add_permissions=None, revoke_permissions=None):
    xml_data = ['<permissionsUpdateRequest><permissionUpdate>']

    xml_data.append(to_xml({'id':document_id, 'type':'DOCUMENT'}, 'entityId'))

    if add_permissions:
        for p in add_permissions:
            xml_data.append(to_xml(p, 'permissionInfo'))
    
    if revoke_permissions:
        for p in revoke_permissions:
            p = p.copy()
            p['permission'] = 'REVOKED'
            p['drm'] = 'NONE'
            xml_data.append(to_xml(p, 'permissionInfo'))
    
    xml_data.append('</permissionUpdate></permissionsUpdateRequest>')

    response = api_client.update(
        '/services/workspaces/permissions', 
        params={
            'workspaceId':exchange_id
        }, 
        data={'xml':''.join(xml_data)},
        api_version=1
    )

    response.check(200, 'text/xml')
    
    data = response.data()

    return data

def update_folder_content_permissions(api_client, exchange_id, folder_id, add_permissions=None, revoke_permissions=None):
    xml_data = ['<permissionsFoldersCreateRequest>']

    xml_data.append(to_xml({'entityId':{'id':document_id, 'type':'DOCUMENT'}}, 'contentIdList'))

    if add_permissions:
        xml_data.append(to_xml([{'permissionInfo': p} for p in add_permissions], 'permissions'))
    
    if revoke_permissions:
        for p in revoke_permissions:
            p = p.copy()
            p['permission'] = 'REVOKED'
            p['drm'] = 'NONE'
            xml_data.append(to_xml(p, 'permissionInfo'))
    
    xml_data.append('</permissionsFoldersCreateRequest>')

    response = api_client.update(
        '/services/workspaces/permissions/folders', 
        params={
            'workspaceId':exchange_id
        }, 
        data={'xml':''.join(xml_data)},
        api_version=1
    )

    response.check(200, 'text/xml')
    
    data = response.data()

def get_permissions2(api_client, exchange_id):
    response = api_client.get(
        '/services/workspaces/permissions', 
        params={
            'workspaceId':exchange_id
        },
        api_version=1
    )

    response.check(200, 'text/xml')

    data = response.data()

    return get_node_as_item(data, 'permissions')