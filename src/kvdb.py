import http.client
import logging as log


class KvdbClient:
    connection = http.client.HTTPSConnection('kvdb.io')

    def __init__(self, bucket_id):
        log.info(f"KVDB {bucket_id} created")
        self.bucket_id = bucket_id

    def set(self, key, value):
        conn = self.connection
        try:
            path = self.build_path(str(key))
            log.info(f"KVDB - PATCH {key}={value}")
            conn.request('POST', path, str(value))
            conn.getresponse().read()
        finally:
            conn.close()

    def get(self, key):
        conn = self.connection
        try:
            conn.request("GET", self.build_path(str(key)))
            data = conn.getresponse().read().decode()
            log.info(f"KVDB - GET {key}={data}")
            return data
        finally:
            conn.close()

    def get_int(self, key):
        data = self.get(key)
        if data is not None and data.isdigit():
            return int(data)
        return None

    def build_path(self, key):
        path = f"/{self.bucket_id}/{key}"
        return path
