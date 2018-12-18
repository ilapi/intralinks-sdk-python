import intralinks_test.documents_helper

def test_create_update_delete_document(v1_client, test_data):
    intralinks_test.documents_helper.test_create_update_delete_document(v1_client, test_data)

def test_create_delete_documents(v1_client, test_data):
    intralinks_test.documents_helper.test_create_delete_documents(v1_client, test_data)

