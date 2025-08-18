import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)
    
    def test_end_slash(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)
    
    def test_http(self):
        input_url = "http://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)
    
    def test_uppercase(self):
        input_url = "http://BLOG.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)
    
    def test_removes_protocol(self):
        self.assertEqual(normalize_url("https://blog.boot.dev/path"), "blog.boot.dev/path")
        self.assertEqual(normalize_url("http://blog.boot.dev/path"), "blog.boot.dev/path")

    def test_removes_trailing_slash(self):
        self.assertEqual(normalize_url("https://blog.boot.dev/path/"), "blog.boot.dev/path")

    def test_handles_mixed_case(self):
        self.assertEqual(normalize_url("https://BLOG.boot.DEV/path"), "blog.boot.dev/path")

    def test_removes_query_params(self):
        self.assertEqual(normalize_url("https://blog.boot.dev/path?query=1"), "blog.boot.dev/path")

    def test_removes_fragments(self):
        self.assertEqual(normalize_url("https://blog.boot.dev/path#section"), "blog.boot.dev/path")

    def test_handles_different_protocols(self):
        self.assertEqual(normalize_url("http://blog.boot.dev/path"), "blog.boot.dev/path")
        self.assertEqual(normalize_url("https://blog.boot.dev/path"), "blog.boot.dev/path")

    def test_handles_empty_path(self):
        self.assertEqual(normalize_url("https://blog.boot.dev"), "blog.boot.dev")
        self.assertEqual(normalize_url("https://blog.boot.dev/"), "blog.boot.dev")

if __name__ == "__main__":
    unittest.main()




