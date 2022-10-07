import http.client


class KvdbClient:
    connection = http.client.HTTPSConnection('kvdb.io')

    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    def set(self, key, value):
        conn = self.connection
        try:
            conn.request('POST', self.build_path(key), value)
            conn.getresponse().read()
        finally:
            conn.close()

    def get(self, key):
        conn = self.connection
        try:
            conn.request("GET", self.build_path(key))
            data = conn.getresponse().read().decode()
            print(f"KVDB - {key}={data} recovered")
            return data
        finally:
            conn.close()

    def get_int(self, key):
        return int(self.get(key))

    def build_path(self, key):
        path = f"/{self.bucket_id}/{key}"
        return path
