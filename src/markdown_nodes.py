
import re
from enum import Enum
from textnode import TextNode, TextType

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

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


def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        split_node = extract_markdown_images(node.text)

        if len(split_node) == 0:
            new_nodes.append(node)
            continue

        for i in range(len(split_node)):
            split_md = f"![{split_node[i][0]}]({split_node[i][1]})"
            sections = remaining.split(split_md, 1)

            if len(sections[0]) != 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(split_node[i][0], TextType.IMAGE, split_node[i][1]))
            remaining = sections[1]
    
        if len(remaining) != 0:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:

        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        split_node = extract_markdown_links(node.text)

        if len(split_node) == 0:
            new_nodes.append(node)
            continue

        for i in range(len(split_node)):
            split_md = f"[{split_node[i][0]}]({split_node[i][1]})"
            sections = remaining.split(split_md, 1)

            if len(sections[0]) != 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(split_node[i][0], TextType.LINK, split_node[i][1]))
            remaining = sections[1]
    
        if len(remaining) != 0:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")
    results = []

    for block in blocks:
        new_block = block.strip()
        if len(new_block) > 0:
            results.append(new_block)
    
    return results


def block_to_block_type(block):

    num_hashes = len(block) - len(block.lstrip("#"))
    lines = block.split("\n")
    
    if 1 <= num_hashes <= 6 and block[num_hashes] == " ":
        return BlockType.HEAD
    
    elif block.startswith ("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    elif all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    
    ordered = True
    for i, line in enumerate(lines):
        if line.startswith(f"{i+1}. "):
            continue
        else:
            ordered = False
            break
    
    if ordered:
        return BlockType.OLIST

    return BlockType.PARA
