import intralinks_test.conftest
from intralinks.functions.entities import ExchangeMember

def test_exchange_members(il, test_data):   
    e = intralinks_test.conftest.test_exchange(il, test_data)

    # Ensure there is just one single member
    ms = il.get_exchange_members(e)
    assert len(ms) == 1, 'The exchange contains {} member(s)'.format(len(ms))
    assert ms[0]['emailId'] == test_data['exchange.owner.email']
    assert ms[0]['roleType'] == 'MANAGER_PLUS'

    # Search for user to add as a member

    u = il.get_user_account(test_data['exchange.new_user.email'], test_data['exchange.id'])
    assert u is not None
    assert u['firstName'] == test_data['exchange.new_user.first_name']
    assert u['lastName'] == test_data['exchange.new_user.last_name']

    # Add the user as a member

    u['emailId'] = u['emailId'].upper()
    m = il.create_exchange_member(e, ExchangeMember(user=u, roleType='REVIEWER'))
    assert m['roleType'] == 'REVIEWER'
    assert m['keyContact'] == False
    assert m['emailId'] == test_data['exchange.new_user.email']

    # Get the member list to ensure the member has been properly added

    ms = il.get_exchange_members(e)
    assert len(ms) == 2
    member_by_email = {m['emailId']:m for m in ms}
    assert test_data['exchange.new_user.email'] in member_by_email
    m = member_by_email[test_data['exchange.new_user.email']]
    assert m['roleType'] == 'REVIEWER'
    assert m['keyContact'] == False

    # Delete the member

    il.delete_exchange_member(e, m)

    # Get the member list to ensure the member has been properly removed

    ms = il.get_exchange_members(e)
    assert len(ms) == 1
    assert ms[0]['emailId'] == test_data['exchange.owner.email']