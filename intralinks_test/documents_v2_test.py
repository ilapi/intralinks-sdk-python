import intralinks_test.documents_helper

def test_documents(v2_client, test_data):
    intralinks_test.documents_helper.test_documents(v2_client, test_data)