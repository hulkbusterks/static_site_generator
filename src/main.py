from textnode import *
def main():
    node = TextNode("this is text node", TextType.bold_text, "https://abc.abc")
    node2 = TextNode("this is text node", TextType.bold_text, "https://abc.abc")
    if node == node2:print("a")
    print(node)
main()
