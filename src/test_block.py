import unittest
from block import markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):

    def test_basic_markdown(self):
        markdown = """
        # Heading 1
        This is a simple paragraph.
        * Item 1
        * Item 2
        1. First ordered item
        2. Second ordered item
        """
        expected_blocks = [
            "# Heading 1",
            "This is a simple paragraph.",
            "* Item 1\n* Item 2",
            "1. First ordered item\n2. Second ordered item"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_blocks)

    def test_empty_markdown(self):
        markdown = ""
        expected_blocks = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_blocks)

    def test_heading_only(self):
        markdown = "# Heading 1"
        expected_blocks = ["# Heading 1"]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_blocks)

    def test_paragraph_only(self):
        markdown = "This is a paragraph."
        expected_blocks = ["This is a paragraph."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_blocks)

    def test_lists_only(self):
        markdown = """
        * Item 1
        * Item 2
        1. First ordered item
        2. Second ordered item
        """
        expected_blocks = [
            "* Item 1\n* Item 2",
            "1. First ordered item\n2. Second ordered item"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_blocks)

    def test_mixed_markdown(self):
        markdown = """
        # Heading 1
        This is a paragraph with some text.
        * Item 1
        * Item 2
        1. Ordered item 1
        2. Ordered item 2
        """
        expected_blocks = [
            "# Heading 1",
            "This is a paragraph with some text.",
            "* Item 1\n* Item 2",
            "1. Ordered item 1\n2. Ordered item 2"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_blocks)

    def test_multiple_empty_lines(self):
        markdown = """
        # Heading 1


        This is a paragraph with excessive newlines.


        * List item 1
        * List item 2


        """
        expected_blocks = [
            "# Heading 1",
            "This is a paragraph with excessive newlines.",
            "* List item 1\n* List item 2"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_blocks)

    def test_trailing_whitespace(self):
        markdown = "This is a paragraph.    "
        expected_blocks = ["This is a paragraph."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_blocks)

    def test_heading(self):
        # Testing different levels of headings
        self.assertEqual(block_to_block_type("# Heading 1"), "heading 1")
        self.assertEqual(block_to_block_type("## Heading 2"), "heading 2")
        self.assertEqual(block_to_block_type("### Heading 3"), "heading 3")
        self.assertEqual(block_to_block_type("#### Heading 4"), "heading 4")

    def test_code(self):
        # Testing a block of code (start with backticks)
        self.assertEqual(block_to_block_type("```python"), "code")
        self.assertEqual(block_to_block_type("`inline code`"), "code")

    def test_quote(self):
        # Testing a blockquote (start with >)
        self.assertEqual(block_to_block_type(
            "> This is a blockquote"), "quote")

    def test_unordered_list(self):
        # Testing unordered lists (start with * or -)
        self.assertEqual(block_to_block_type("* Item 1"), "unordered_list")
        self.assertEqual(block_to_block_type("- Item 2"), "unordered_list")

    def test_ordered_list(self):
        # Testing ordered lists (start with number and period)
        self.assertEqual(block_to_block_type("1. First item"), "ordered_list")
        self.assertEqual(block_to_block_type("2. Second item"), "ordered_list")

    def test_paragraph(self):
        # Testing paragraphs (should return 'paragraph' for regular text)
        self.assertEqual(block_to_block_type(
            "This is a regular paragraph"), "paragraph")
        self.assertEqual(block_to_block_type(
            "Another simple paragraph."), "paragraph")

    def test_simple_paragraph(self):
        markdown = "This is a simple paragraph."
        expected_html = "<div><p>This is a simple paragraph.</p></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)

    def test_heading_html(self):
        markdown = "# Heading 1"
        expected_html = "<div><h1>Heading 1</h1></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)

    def test_bold_text(self):
        markdown = "This is **bold**."
        expected_html = "<div><p>This is <b>bold</b>.</p></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)

    def test_italic_text(self):
        markdown = "This is *italic*."
        expected_html = "<div><p>This is <i>italic</i>.</p></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)

    def test_link(self):
        markdown = "This is a [link](https://example.com)."
        expected_html = "<div><p>This is a <a href=\"https://example.com\">link</a>.</p></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)

    def test_image(self):
        markdown = "This is an image: ![Alt Text](https://example.com/image.png)"
        expected_html = "<div><p>This is an image: <img src=\"https://example.com/image.png\" alt=\"Alt Text\"></img></p></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)

    def test_ordered_list_html(self):
        markdown = "1. First item\n2. Second item"
        expected_html = "<div><ol><li>First item</li><li>Second item</li></ol></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)

    def test_unordered_list_html(self):
        markdown = "- Item 1\n- Item 2"
        expected_html = "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)

    def test_quote_html(self):
        markdown = "> This is a quote."
        expected_html = "<div><blockquote>This is a quote.</blockquote></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)


if __name__ == '__main__':
    unittest.main()
