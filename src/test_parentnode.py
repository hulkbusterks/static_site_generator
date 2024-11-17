import unittest
from unittest.mock import MagicMock
from htmlnode import HTMLNode
from LeafNode import LeafNode
from parentnode import ParentNode 

class TestParentNode(unittest.TestCase):

    def setUp(self):
        # Mock or create basic LeafNode instances
        self.mock_leaf1 = MagicMock(spec=LeafNode)
        self.mock_leaf2 = MagicMock(spec=LeafNode)
        self.mock_leaf1.to_html.return_value = "<p>Leaf 1</p>"
        self.mock_leaf2.to_html.return_value = "<span>Leaf 2</span>"

    def test_parent_node_initialization(self):
        # Test with valid inputs
        parent_node = ParentNode("div", [self.mock_leaf1, self.mock_leaf2])
        self.assertEqual(parent_node.tag, "div")
        self.assertEqual(len(parent_node.children), 2)

    def test_invalid_parent_node_tag(self):
        # Test when no tag is provided (should raise ValueError)
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [self.mock_leaf1, self.mock_leaf2])

        # Check that the exception message is correct
        self.assertEqual(str(context.exception), "no tag received")

    def test_invalid_parent_node_children(self):
        # Test when no children are provided (should raise ValueError)
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)

        # Check that the exception message is correct
        self.assertEqual(str(context.exception), "parent needs at least one child")

    def test_empty_children(self):
        # Test with an empty list of children (should raise ValueError)
        with self.assertRaises(ValueError) as context:
            ParentNode("div", [])

        # Check that the exception message is correct
        self.assertEqual(str(context.exception), "parent needs at least one child")

    def test_to_html_valid(self):
        # Test the output of to_html with valid children
        parent_node = ParentNode("div", [self.mock_leaf1, self.mock_leaf2])
        expected_html = "<div><p>Leaf 1</p><span>Leaf 2</span></div>"
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_to_html_invalid_tag(self):
        # Test calling to_html with a ParentNode that has no tag
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [self.mock_leaf1, self.mock_leaf2])

        self.assertEqual(str(context.exception), "no tag received")

    def test_to_html_no_children(self):
        # Test calling to_html with no children
        with self.assertRaises(ValueError) as context:
            ParentNode("div", [])

        self.assertEqual(str(context.exception), "parent needs at least one child")

    def test_to_html_single_child(self):
        # Test with only one child
        parent_node = ParentNode("ul", [self.mock_leaf1])
        expected_html = "<ul><p>Leaf 1</p></ul>"
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_to_html_empty_tag(self):
        # Test for an edge case of having an empty tag
        with self.assertRaises(ValueError) as context:
            ParentNode("", [self.mock_leaf1])

        self.assertEqual(str(context.exception), "no tag received")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == '__main__':
    unittest.main()

