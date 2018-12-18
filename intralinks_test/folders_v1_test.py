import intralinks_test.folders_helper

def test_create_update_delete_folder(v1_client, test_data):
    intralinks_test.folders_helper.test_create_update_delete_folder(v1_client, test_data)

def test_create_delete_folders(v1_client, test_data):
    intralinks_test.folders_helper.test_create_delete_folders(v1_client, test_data)

