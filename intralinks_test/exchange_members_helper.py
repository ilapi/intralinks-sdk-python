import intralinks_test.conftest
from intralinks.functions.entities import ExchangeMember

def test_exchange_members(il, test_data):   
    e = intralinks_test.conftest.test_exchange(il, test_data)

    # Ensure there is just one single member
    ms = il.get_exchange_members(e)
    assert len(ms) == 1, 'The exchange contains {} member(s)'.format(len(ms))
    assert ms[0]['emailId'] == test_data['exchange.owner.email']
    assert ms[0]['roleType'] == 'MANAGER_PLUS'

    # Add a user as a member

    u = {
        'emailId':test_data['exchange.new_user.email'].upper(),
        'firstName':test_data['exchange.new_user.first_name'],
        'lastName':test_data['exchange.new_user.last_name'],
        'officePhone':test_data['exchange.new_user.phone'],
        'organization':test_data['exchange.new_user.organization']
    }

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

    # Update the member

    m['roleType'] = 'MANAGER_PLUS'
    m = il.update_exchange_member(e, m)
    assert m['roleType'] == 'MANAGER_PLUS'

    # Get the member list to ensure the member has been properly added

    ms = il.get_exchange_members(e)
    assert len(ms) == 2
    member_by_email = {m['emailId']:m for m in ms}
    assert test_data['exchange.new_user.email'] in member_by_email
    m = member_by_email[test_data['exchange.new_user.email']]
    assert m['roleType'] == 'MANAGER_PLUS'
    assert m['keyContact'] == False

    # Delete the member

    il.delete_exchange_member(e, m)

    # Get the member list to ensure the member has been properly removed

    ms = il.get_exchange_members(e)
    assert len(ms) == 1
    assert ms[0]['emailId'] == test_data['exchange.owner.email']