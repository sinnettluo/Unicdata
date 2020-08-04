import hashlib
import os

from redis import ConnectionPool, StrictRedis
from w3lib.url import canonicalize_url

__author__ = 'cagey'
from scrapy.dupefilters import RFPDupeFilter


class URLRedisFilter(RFPDupeFilter):
    """ 只根据url去重"""

    def __init__(self, path=None, debug=False):
        RFPDupeFilter.__init__(self, path)
        self.dupefilter = UrlFilterAndAdd()

    def request_seen(self, request):
        # 校验，新增2行代码
        if self.dupefilter.check_url(request.url):
            return True

        # 保留中间页面的去重规则不变，不然爬虫在运行过程中容易出现死循环
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)


class UrlFilterAndAdd(object):
    def __init__(self, host, key, db):
        redis_config = {
            "host": host,  # redis ip
            "port": 6379,
            "password": None,
            "db": db,
        }

        pool = ConnectionPool(**redis_config)
        self.pool = pool
        self.redis = StrictRedis(connection_pool=pool)
        self.key = key

    def url_sha1(self, url):
        fp = hashlib.sha1()
        fp.update(canonicalize_url(url).encode("utf-8"))
        url_sha1 = fp.hexdigest()
        return url_sha1

    def check_url(self, url):
        sha1 = self.url_sha1(url)
        # 此处只判断url是否在set中，并不添加url信息，
        # 防止将起始url 、中间url(比如列表页的url地址)写入缓存中，
        isExist = self.redis.sismember(self.key, sha1)
        return isExist

    def add_url(self, url):
        sha1 = self.url_sha1(url)
        added = self.redis.sadd(self.key, sha1)
        return added