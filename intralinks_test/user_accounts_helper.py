import intralinks_test.conftest

def test_user_accounts(il, test_data):
    u = il.get_user_account(test_data['exchange.new_user.email'], test_data['exchange.id'])
    assert u is not None
    assert u['firstName'] == test_data['exchange.new_user.first_name']
    assert u['lastName'] == test_data['exchange.new_user.last_name']