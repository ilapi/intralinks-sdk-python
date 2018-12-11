import intralinks_test.groups_helper

def test_groups(v2_client, test_data):
    intralinks_test.groups_helper.test_groups(v2_client, test_data)