from context import database

store = database.redis_store.redis_store()

test_from_key = "test_from_fake_key"
test_to_key = "test_to_fake_key"


def test_basic_storage():
    prior = int(store.get_weights(test_from_key).get(test_to_key.encode('UTF-8'),0))
    update = store.update_weight(test_from_key, test_to_key, 1)
    final = int(store.get_weights(test_from_key).get(test_to_key.encode('UTF-8'),0))
    assert final == update
    assert final == (prior + 1)


if __name__ == '__main__':
    test_basic_storage()