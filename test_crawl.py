import unittest
from crawl import normalize_url, get_urls_from_html


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
    
    def test_get_urlss_from_html(self):
        html = """
        <html>
            <body>
                <a href="https://blog.boot.dev">Absolute Link</a>
                <a href="/path/to/page">Relative Link</a>
                <a href="invalid-url">Invalid Link</a>
            </body>
        </html>
        """
        base_url = "https://blog.boot.dev"
        
        # Test absolute URL extraction
        urls = get_urls_from_html(html, base_url)
        self.assertIn("https://blog.boot.dev", urls)
        
        # Test relative URL joining
        self.assertIn("https://blog.boot.dev/path/to/page", urls)
        
        # Test invalid URL handling
        self.assertEqual(len(urls), 2)  # Should skip invalid-url

    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev></span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html(self):
        html = """
        <html>
            <body>
                <a href="https://blog.boot.dev">Absolute Link</a>
                <a href="/path/to/page">Relative Link</a>
                <a href="invalid-url">Invalid Link</a>
                <a href="">Empty Link</a>
                <a href="  ">Whitespace Link</a>
                <a href="#section">Fragment Link</a>
            </body>
        </html>
        """
        base_url = "https://blog.boot.dev"
        
        urls = get_urls_from_html(html, base_url)
        self.assertEqual(len(urls), 2)  # Should only keep the absolute and relative links
        self.assertIn("https://blog.boot.dev", urls)
        self.assertIn("https://blog.boot.dev/path/to/page", urls)

    
        
if __name__ == "__main__":
    unittest.main()




