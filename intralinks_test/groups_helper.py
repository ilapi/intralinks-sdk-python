import intralinks_test.conftest
from intralinks.functions.entities import Group

def test_groups(il, test_data):
    e = intralinks_test.conftest.test_exchange(il, test_data)

    #%% [markdown]
    # Check that there is no groups

    #%%
    gs = il.get_groups(e)
    assert len(gs) == 0, 'The exchange contains {} group(s)'.format(len(gs))

    #%% [markdown]
    # A tester: différent type de groupe, ftsEnabled, defaultFolderPath
    #%% [markdown]
    # Let's create a group (without a note)...

    #%%
    g = il.create_group(e, Group('Group 1', groupType='WORKSPACE', note=None, ftsEnabled=False, defaultFolderPath=None))
    assert g['groupName'] == 'Group 1'
    assert g['groupType'] == 'WORKSPACE'
    assert g['ftsEnabled'] == False
    assert 'note' not in g
    assert 'defaultFolderPath' not in g

    #%% [markdown]
    # ... and check that the group has been created properly

    #%%
    gs = il.get_groups(e)
    assert len(gs) == 1
    g = gs[0]
    assert g['groupName'] == 'Group 1'
    assert g['groupType'] == 'WORKSPACE'
    assert g['ftsEnabled'] == False
    assert g['note'] == ' '
    assert 'defaultFolderPath' not in g

    #%% [markdown]
    # Let's update the group...

    #%%
    g['groupName'] = 'Update Group 1'
    g['note'] = 'a' * 200
    g = il.update_group(e, g)
    assert g['groupName'] == 'Update Group 1'
    assert g['groupType'] == 'WORKSPACE'
    assert g['ftsEnabled'] == False
    assert g['note'] == 'a' * 200
    assert 'defaultFolderPath' not in g

    #%% [markdown]
    # ... and check the group has been updated properly

    #%%
    gs = il.get_groups(e)
    assert len(gs) == 1
    g = gs[0]
    assert g['groupName'] == 'Update Group 1'
    assert g['groupType'] == 'WORKSPACE'
    assert g['ftsEnabled'] == False
    assert g['note'] == 'a' * 200
    assert 'defaultFolderPath' not in g

    #%% [markdown]
    # Delete the group and check it has been deleted

    #%%
    il.delete_group(e, g)
    gs = il.get_groups(e)
    assert len(gs) == 0

    #%% [markdown]
    # Let's create a group with a note...

    #%%
    g = il.create_group(e, Group('Group 2', groupType='WORKSPACE', note='une note', ftsEnabled=False, defaultFolderPath=None))
    assert g['groupName'] == 'Group 2'
    assert g['groupType'] == 'WORKSPACE'
    assert g['ftsEnabled'] == False
    assert g['note'] == 'une note'
    assert 'defaultFolderPath' not in g

    #%% [markdown]
    # ... and check the group has been created properly

    #%%
    gs = il.get_groups(e)
    assert len(gs) == 1
    g = gs[0]
    assert g['groupName'] == 'Group 2'
    assert g['groupType'] == 'WORKSPACE'
    assert g['ftsEnabled'] == False
    assert g['note'] == 'une note'
    assert 'defaultFolderPath' not in g

    #%% [markdown]
    # Delete the group and check it has been deleted

    #%%
    il.delete_group(e, g)
    gs = il.get_groups(e)
    assert len(gs) == 0