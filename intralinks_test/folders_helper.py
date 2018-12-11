import intralinks_test.conftest
from intralinks.functions.entities import Folder

def test_folders(il, test_data):
    e = intralinks_test.conftest.test_exchange(il, test_data)

    #%% [markdown]
    # Check that there is no folders

    #%%
    fs = il.get_folders(e)
    assert len(fs) == 0, 'The exchange contains {} folder(s)'.format(len(fs))
    
    #%% [markdown]
    # Create a folder

    #%%
    f = il.create_folder(e, Folder('Folder 1'))
    id1 = f['id']
    assert f['name'] == 'Folder 1'
    assert f['hasNote'] == False
    assert f['indexingDisabled'] == False

    #%% [markdown]
    # Get the folder to check it has been created properly

    #%%
    fs = il.get_folders(e)
    assert len(fs) == 1
    f = fs[0]
    assert f['id'] == id1
    assert f['name'] == 'Folder 1'
    # assert f['hasNote'] == False # The note field is not retrieved the v2 api
    assert 'note' not in f # The note field is not retrieved by a call to il.get_folders()
    assert f['indexingDisabled'] == False


    #%%
    f['name'] = 'Updated Folder 1'
    f['note'] = 'une note'
    f = il.update_folder(e, f)
    assert f['name'] == 'Updated Folder 1'
    assert f['hasNote'] == True
    assert f['indexingDisabled'] == False


    #%%
    fs = il.get_folders(e)
    assert len(fs) == 1
    f = fs[0]
    assert f['id'] == id1
    assert f['name'] == 'Updated Folder 1'
    #assert f['hasNote'] == True # The note field is not retrieved the v2 api
    assert 'note' not in f # The note field is not retrieved by a call to il.get_folders()
    assert f['indexingDisabled'] == False

    #%% [markdown]
    # Warning: The note field is not retrieved by a call to il.get_folders()
    # 
    # Should I use https://services.intralinks.com/services/workspaces/folders/note
    # 
    # Warning: the hasNote field is not retrieved by a call to il.get_folders() V2

    #%%
    il.delete_folder(e, f)
    fs = il.get_folders(e)
    assert len(fs) == 0
