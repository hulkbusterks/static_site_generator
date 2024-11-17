from htmlnode import HTMLNode
from LeafNode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        if not tag: raise ValueError("no tag received")
        if children == None or children == []: raise ValueError("parent needs at least one child")
        super().__init__(tag = tag, children = children, props = props)
    
    def to_html(self):
        if self.tag == None: raise ValueError("no tag received")
        if self.children == None or self.children == []: raise ValueError("parent node needs children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"   
