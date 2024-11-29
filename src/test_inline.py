import unittest
from textnode import *
from inline import *

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_with_bold(self):
        node = TextNode("This is *bold* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_with_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_invalid_syntax(self):
        node = TextNode("This is text with no ending delimiter *bold", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid markdown syntax")

    def test_multiple_delimiters(self):
        node = TextNode("This is *bold* and `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " text")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        # Test case 1: Single image
        text = "Here is an image ![Alt Text](http://example.com/image.jpg)."
        result = extract_markdown_images(text)
        expected = [('Alt Text', 'http://example.com/image.jpg')]
        self.assertEqual(result, expected)

        # Test case 2: Multiple images
        text = """
        ![Image 1](http://example.com/image1.jpg)
        ![Image 2](http://example.com/image2.jpg)
        """
        result = extract_markdown_images(text)
        expected = [
            ('Image 1', 'http://example.com/image1.jpg'),
            ('Image 2', 'http://example.com/image2.jpg')
        ]
        self.assertEqual(result, expected)

        # Test case 3: No images
        text = "There are no images here."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        # Test case 1: Single link
        text = "Here is a [link](http://example.com)."
        result = extract_markdown_links(text)
        expected = [('link', 'http://example.com')]
        self.assertEqual(result, expected)

        # Test case 2: Multiple links
        text = """
        [Google](http://google.com)
        [Example](http://example.com)
        """
        result = extract_markdown_links(text)
        expected = [
            ('Google', 'http://google.com'),
            ('Example', 'http://example.com')
        ]
        self.assertEqual(result, expected)

        # Test case 3: No links
        text = "There are no links here."
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

    def test_mixed_content(self):
        text = """
        This is a [link](http://example.com).
        And this is an image ![Image](http://example.com/image.jpg).
        """

        # Extracting images
        result_images = extract_markdown_images(text)
        expected_images = [('Image', 'http://example.com/image.jpg')]

        # Extracting links
        result_links = extract_markdown_links(text)
        expected_links = [('link', 'http://example.com')]
    
        # Assertions
        self.assertEqual(result_images, expected_images)
        self.assertEqual(result_links, expected_links)
    
    def test_invalid_markdown(self):
        # Test case for invalid markdown (no closing parentheses)
        text = "This is a malformed image ![Alt Text](http://example.com/image.jpg"
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

        # Test case for invalid link (no closing parenthesis)
        text = "This is a malformed link [Google](http://google.com"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()

