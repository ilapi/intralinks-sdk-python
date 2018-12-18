import intralinks_test.conftest
from intralinks.functions.entities import Folder

def precondition(il, e):
    fs = il.get_folders(e)
    assert len(fs) == 0, 'The exchange contains {} folder(s)'.format(len(fs))

def test_create_update_delete_folder(il, test_data):
    e = intralinks_test.conftest.test_exchange(il, test_data)

    precondition(il, e)

    # Create a folder

    f = il.create_folder(e, Folder('Folder 1'))
    id1 = f['id']
    assert f['name'] == 'Folder 1'
    assert f['hasNote'] == False
    assert f['indexingDisabled'] == False

    # Get the folder to check it has been created properly

    fs = il.get_folders(e)
    assert len(fs) == 1
    f = fs[0]
    assert f['id'] == id1
    assert f['name'] == 'Folder 1'
    # assert f['hasNote'] == False # The note field is not retrieved the v2 api
    assert 'note' not in f # The note field is not retrieved by a call to il.get_folders()
    assert f['indexingDisabled'] == False

    # Update the folder

    f['name'] = 'Updated Folder 1'
    f['note'] = 'une note'
    f = il.update_folder(e, f)
    assert f['name'] == 'Updated Folder 1'
    assert f['hasNote'] == True
    assert f['indexingDisabled'] == False


    # Get the folder to check it has been updated properly

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

    # Delete the folder

    il.delete_folder(e, f)
    fs = il.get_folders(e)
    assert len(fs) == 0

def test_create_delete_folders(il, test_data):
    e = intralinks_test.conftest.test_exchange(il, test_data)

    precondition(il, e)
 
    fs = il.create_folders(e, [Folder('Folder 1'),  Folder('Folder 2'), Folder('Folder 3')])
    for f in fs:
        assert 'id' in f

    folders = il.get_folders(e)
    assert len(folders) == 3
    assert len({f['name'] for f in folders}.difference({'Folder 1', 'Folder 2', 'Folder 3'})) == 0

    sfs = il.create_folders(e, [Folder('Subf{}.1'.format(f['name'][1:]), f['id']) for f in fs])
    for f in sfs:
        assert 'id' in f

    folders = il.get_folders(e)
    assert len(folders) == 6
    assert len({f['name'] for f in folders}.difference({'Folder 1', 'Folder 2', 'Folder 3', 'Subfolder 1.1', 'Subfolder 2.1', 'Subfolder 3.1'})) == 0

    # delete the root folders
    il.delete_folders(e, [f for f in folders if 'parentId' not in f])

    folders = il.get_folders(e)
    assert len(folders) == 0
