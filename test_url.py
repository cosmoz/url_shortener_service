import unittest
from unittest.mock import patch, MagicMock


class MockRedis:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value):
        self.store[key] = value


class TestApp(unittest.TestCase):
    def setUp(self):
        self.mock_redis = MockRedis()

        import url as url_module
        self._patcher = patch.object(url_module, "r", self.mock_redis)
        self._patcher.start()

        from url import app
        self.app = app
        self.client = self.app.test_client()

    def tearDown(self):
        self._patcher.stop()

    def test_main_page(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_redirect_missing_key(self):
        resp = self.client.get("/12345/")
        self.assertEqual(resp.status_code, 404)

    def test_redirect_existing_key(self):
        self.mock_redis.set(12345, "https://example.com")
        resp = self.client.get("/12345/")
        self.assertEqual(resp.status_code, 302)

    def test_shorten_bad_url(self):
        resp = self.client.post("/shorten/", data={"url": "not-a-url"})
        self.assertEqual(resp.status_code, 400)

    def test_shorten_empty_url(self):
        resp = self.client.post("/shorten/", data={"url": ""})
        self.assertEqual(resp.status_code, 400)

    def test_shorten_valid_url(self):
        resp = self.client.post("/shorten/", data={"url": "https://example.com"})
        self.assertEqual(resp.status_code, 200)
        key = resp.data.decode().strip()
        self.assertTrue(len(key) > 0)

    def test_shorten_same_url_same_key(self):
        url = "https://example.com/path"
        r1 = self.client.post("/shorten/", data={"url": url}).data.decode().strip()
        r2 = self.client.post("/shorten/", data={"url": url}).data.decode().strip()
        self.assertEqual(r1, r2)

    def test_shorten_key_is_unsigned(self):
        resp = self.client.post("/shorten/", data={"url": "https://example.com"})
        key = resp.data.decode().strip()
        self.assertEqual(int(key), int(key) & 0xFFFFFFFF)


if __name__ == "__main__":
    unittest.main()
