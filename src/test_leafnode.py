from LeafNode import LeafNode

import unittest

class TestLeafNode(unittest.TestCase):
    
    def test_leaf_node_with_value(self):
        # Test: Simple leaf node with a tag
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")
        
    def test_leaf_node_with_attributes(self):
        # Test: Leaf node with a tag and attributes
        node = LeafNode("a", "Click here", {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click here</a>')
        
    def test_leaf_node_without_tag(self):
        # Test: Leaf node without a tag (raw text)
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text") 
    
    def test_leaf_node_with_empty_attributes(self):
        # Test: Should handle empty attributes gracefully
        node = LeafNode("img", "", {"src": "image.png"})
        self.assertEqual(node.to_html(), '<img src="image.png"></img>')

if __name__ == "__main__":
    unittest.main()

