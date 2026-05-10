
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        raise Exception("Node list is empty")
    if delimiter is None:
        raise Exception("Missing delimiter")
    if text_type is None:
        raise Exception("Missing text type")
    
    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        split_node = node.text.split(delimiter)

        if len(split_node)%2 == 0:
            raise Exception("Invalid Markdown: no closing delimiter")

        for i in range(len(split_node)):
            if len(split_node[i]) == 0:
                continue
            if i%2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_node[i], text_type))
    
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

