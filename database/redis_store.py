import redis
import utils
import random
import logging

logger = logging.getLogger(__name__)

"Interface to persistent datastore."


class redis_store(object):

    def __init__(self):
        self._redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def delete_all_in_redis_be_careful(self):
        self._redis.flushdb()

    def get_weights(self, key):
        return self._redis.hgetall(key)

    def update_weight(self, node_from, node_to, weight):
        new_val = self._redis.hincrby(node_from, node_to, weight)
        if new_val <= 0:
            self._redis.hdel(node_from, node_to)
        return new_val

    def append_ner(self, entities):
        for ner_type in [utils.ner_per, utils.ner_org, utils.ner_loc]:
            for entity in entities[ner_type]:
                self._redis.rpush(ner_type, entity)

    def unappend_ner(self, entities):
        "Remove one copy of each entity in the list"
        for ner_type in [utils.ner_per, utils.ner_org, utils.ner_loc]:
            for entity in entities[ner_type]:
                self._redis.lrem(ner_type, 1, entity)

    def add_source(self, source_name):
        self._redis.rpush(self._source_field, source_name)

    def remove_source(self, source_name):
        self._redis.lrem(self._source_field, -1, source_name)

    def random_entry(self):
        "Make sure random entry is not a special token (e.g. sentence-start)"
        while True:
            s = self._redis.randomkey().decode("utf-8")
            if not(s.startswith(utils.START_TOKEN) or s.startswith(utils.END_TOKEN)):
                break
        return s[0:s.rfind(":")].split("|")

    def random_entity(self, ner_type):
        """Returns random entity of specified type"""
        type_count = self._redis.llen(ner_type)
        if type_count > 0:
            idx = random.randint(0, type_count - 1)
            return(self._redis.lindex(ner_type, idx).decode('UTF-8'))
        else:
            logger.info("No entity in Redis store for type {}".format(ner_type))
            return ""

    # TODO: Add check_source() which returns true iif source_name is in list already
    # Use it to stop loading same doc twice. Also probably a source_report fn.

    def ner_report(self, n=2):
        print(self._redis.lrange(self._ner_per, 0, n))
        print(self._redis.lrange(self._ner_org, 0, n))
        print(self._redis.lrange(self._ner_loc, 0, n))
