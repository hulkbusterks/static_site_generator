from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            x = node.text.split(delimiter)
            if len(x)%2 == 0: raise Exception("Invalid markdown syntax")
            for i in range(len(x)):
                if i%2 != 0: new_nodes.append(TextNode(x[i], text_type))
                else: new_nodes.append(TextNode(x[i], TextType.TEXT))
        else: new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    image_pattern = r"!\[([^\]]*)\]\((.*?)\)"
    matches = re.findall(image_pattern, text)
    return matches  

def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(link_pattern, text)
    return matches
