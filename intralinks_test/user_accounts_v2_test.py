import intralinks_test.user_accounts_helper

def test_groups(v2_client, test_data):
    intralinks_test.user_accounts_helper.test_user_accounts(v2_client, test_data)
