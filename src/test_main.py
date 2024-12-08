import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_valid_h1(self):
        markdown = "# Hello World\nSome other content."
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_valid_h1_with_leading_space(self):
        markdown = "#   Leading Spaces\nContent follows."
        self.assertEqual(extract_title(markdown), "Leading Spaces")

    def test_valid_h1_with_trailing_space(self):
        markdown = "# Trailing Spaces   \nMore content."
        self.assertEqual(extract_title(markdown), "Trailing Spaces")

    def test_multiple_headers(self):
        markdown = "# First Header\n## Second Header\nContent."
        self.assertEqual(extract_title(markdown), "First Header")

    def test_no_h1_header(self):
        markdown = "## No H1 Here\nContent."
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception),
                         "Title must have h1 tag")

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception),
                         "Title must have h1 tag")


if __name__ == '__main__':
    unittest.main()
