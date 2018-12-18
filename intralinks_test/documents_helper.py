import intralinks_test.conftest
from intralinks.functions.entities import Folder, Document

def precondition(il, e):
    ds = il.get_documents(e)
    assert len(ds) == 0, 'The exchange contains {} document(s)'.format(len(ds))

    fs = il.get_folders(e)
    assert len(fs) == 0, 'The exchange contains {} folders(s)'.format(len(fs))

def test_create_update_delete_document(il, test_data):
    e = intralinks_test.conftest.test_exchange(il, test_data)

    precondition(il, e)

    # Scenario
    # 1. Create a folder
    # 2. Create a document
    # 3. Get the documents to check creation succeeded
    # 4. Delete the document
    # 5. Get the documents to check deletion succeeded

    # 1. Create a folder
    f = il.create_folder(e, Folder('Folder for doc'))
    fs = il.get_folders(e)
    assert len(fs) == 1
    f = fs[0]
    assert f['name'] == 'Folder for doc'

    # 2. Create a document
    d = il.create_document(e, Document('Document 1', f['id']))
    id1 = d['id']
    assert d['name'] == 'Document 1'

    # 3. Get the documents to check creation succeeded
    ds = il.get_documents(e)
    assert len(ds) == 1
    d = ds[0]
    assert d['id'] == id1
    assert d['name'] == 'Document 1'
    assert d['hasNote'] == False
    assert d['parentId'] == f['id']

    # 4. Delete the document
    il.delete_document(e, d)

    # 5. Get the documents to check deletion succeeded
    ds = il.get_documents(e)
    assert len(ds) == 0

    #%%
    d = il.create_document(e, Document('Document 2', f['id']))

    ds = il.get_documents(e)
    assert len(ds) == 1
    d = ds[0]
    assert d['name'] == 'Document 2'

    d['name'] = 'New Document 2'
    d = il.update_document(e, d)
    assert d['name'] == 'New Document 2'

    ds = il.get_documents(e)
    assert len(ds) == 1
    d = ds[0]
    assert d['name'] == 'New Document 2'

    #%%
    il.delete_document(e, d)
    ds = il.get_documents(e)
    assert len(ds) == 0

    #%%
    il.delete_folder(e, f)
    fs = il.get_folders(e)
    assert len(fs) == 0

def test_create_delete_documents(il, test_data):
    e = intralinks_test.conftest.test_exchange(il, test_data)

    precondition(il, e)

    # 1. Create folders
    il.create_folders(e, [Folder('Folder for doc 1'), Folder('Folder for doc 2')])
    fs = il.get_folders(e)
    assert len(fs) == 2

    # x. Create documents
    documents = [Document('Document {}'.format(i) , f['id']) for i, f in enumerate(fs)]
    il.create_documents(e, documents)
    ds = il.get_documents(e)
    assert len(documents) == len(ds)

    # x. Delete the documents
    il.delete_documents(e, ds)
    ds = il.get_documents(e)
    assert len(ds) == 0

    # x. Delete the folders
    il.delete_folders(e, fs)
    fs = il.get_folders(e)
    assert len(fs) == 0

