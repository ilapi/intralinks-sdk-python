import intralinks_test.documents_helper

def test_create_update_delete_document(v2_client, test_data):
    intralinks_test.documents_helper.test_create_update_delete_document(v2_client, test_data)

def test_create_test_create_delete_documentsupdate_delete_document(v2_client, test_data):
    intralinks_test.documents_helper.test_create_delete_documents(v2_client, test_data)