# -*- encoding: utf-8 -*-

import redis

_conn = None


class RedisUtils(object):

  def __init__(self, host, port, db, password):
    self._pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)

  def _get_redis(self):
    return redis.Redis(connection_pool=self._pool)

  def get(self, key):
    r = self._get_redis()
    return r.get(key)

  def set(self, key, val, time=0):
    r = self._get_redis()
    if time <= 0:
      r.set(key, val)
    else:
      r.setex(key, val, time)


_redis_map = {}


def get_redis_utils(host, port, db, password):
  global _redis_map
  key = '%s:%d:%d' % (host, port, db)
  if None is _redis_map.get(key, None):
    _redis_map[key] = RedisUtils(host, port, db, password)

  return _redis_map[key]
