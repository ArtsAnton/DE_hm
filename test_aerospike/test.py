import aerospike
from aerospike import exception as ex
from aerospike import predicates as p
import logging

config = {'hosts': [('127.0.0.1', 3000)]}
client = aerospike.client(config)
client.connect()
print('Connect:', client.is_connected())


def add_customer(customer_id, phone_number, lifetime_value, namespace='test', aero_set='demo'):
    key = (namespace, aero_set, customer_id)
    bins = {
        'phone': phone_number,
        'ltv': lifetime_value
    }
    client.put(key, bins)


def get_ltv_by_id(customer_id, namespace='test', aero_set='demo'):
    key = (namespace, aero_set, customer_id)
    try:
        (key, metadata, record) = client.get(key)
        return record['ltv']
    except ex.RecordNotFound:
        logging.error('Requested non-existent customer ' + str(customer_id))


def get_ltv_by_phone(phone_number, namespace='test', aero_set='demo'):
    query = client.query(namespace, aero_set)
    query.select('ltv')
    query.where(p.equals('phone', phone_number))
    try:
        (key, metadata, record) = query.results()[0]
        return record['ltv']
    except IndexError:
        logging.error('Requested phone number is not found ' + str(phone_number))


for i in range(0, 1000):
    add_customer(i, i, i + 1)
client.index_integer_create('test', 'demo', 'phone', 'index_phone')
# client.index_remove('test', 'index_phone')

for i in range(0, 1005):
    assert (i + 1 == get_ltv_by_id(i)), "No LTV by ID " + str(i)
    assert (i + 1 == get_ltv_by_phone(i)), "No LTV by phone " + str(i)
