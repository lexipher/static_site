import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_link_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Look at me!")
        self.assertEqual(node.to_html(), '<b>Look at me!</b>')

class TestHTMLNode(unittest.TestCase):
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

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_multiple_children(self):
        child_node_1 = LeafNode("b", "child 1")
        child_node_2 = LeafNode("i", "child 2")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child 1</b><i>child 2</i></div>",
        )

class TestParentNode(unittest.TestCase):
    def test_parent_with_multiple_children(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, " normal "),
            LeafNode("i", "italic"),
        ])
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b> normal <i>italic</i></p>"
        )

    def test_parent_with_props(self):
        node = ParentNode("div", [LeafNode(None, "hello")], {"class": "box"})
        self.assertEqual(
            node.to_html(),
            '<div class="box">hello</div>'
        )

    def test_parent_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a BOLD text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a BOLD text node")

    def test_italic_text(self):
        node = TextNode("This is an ITALIC text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an ITALIC text node")

    def test_code_text(self):
        node = TextNode("This is a CODE text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a CODE text node")

    def test_link(self):
        node = TextNode("This is a LINK node", TextType.LINK, "https://www.boot.dev/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev/"})
        self.assertEqual(html_node.value, "This is a LINK node")

    def test_image(self):
        node = TextNode("This is an IMAGE node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-150.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/img/bootdev-logo-full-150.png", "alt": "This is an IMAGE node"})
        self.assertEqual(html_node.value, "")

class TestSplitTextNode(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("This is a text node with no markdown", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, 
            [
            TextNode("This is a text node with no markdown", TextType.TEXT)
            ]
        )

    def test_code_text(self):
        node = TextNode("This is a text node with `code` markdown", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(split_nodes, 
            [
            TextNode("This is a text node with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" markdown", TextType.TEXT)
            ]
        )

    def test_bold_text(self):
        node = TextNode("This is a text node with **bold** markdown", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, 
            [
            TextNode("This is a text node with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" markdown", TextType.TEXT)
            ]
        )

    def test_italic_text(self):
        node = TextNode("This is a text node with _italic_ markdown", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(split_nodes, 
            [
            TextNode("This is a text node with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" markdown", TextType.TEXT)
            ]
        )

    def test_bold_start_text(self):
        node = TextNode("**This is a text node that starts with bold** markdown", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, 
            [
            TextNode("This is a text node that starts with bold", TextType.BOLD),
            TextNode(" markdown", TextType.TEXT)
            ]
        )

    def test_italic_end_text(self):
        node = TextNode("This is a text node that ends with _italic markdown_", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(split_nodes, 
            [
            TextNode("This is a text node that ends with ", TextType.TEXT),
            TextNode("italic markdown", TextType.ITALIC),
            ]
        )

    def test_unchanged_text(self):
        node = TextNode("This is not a plain text node", TextType.BOLD)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, 
            [
            TextNode("This is not a plain text node", TextType.BOLD)
            ]
        )

    def test_invalid_markdown(self):
        node = TextNode("This is a text node with _invalid markdown", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

class TestMarkdownExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_skips_images(self):
        matches = extract_markdown_links(
            "![image](https://example.com/img.png) and [a link](https://example.com)"
        )
        self.assertListEqual([("a link", "https://example.com")], matches)

    def test_extract_markdown_images_skips_links(self):
        matches = extract_markdown_images(
            "![image](https://example.com/img.png) and [a link](https://example.com)"
        )
        self.assertListEqual([("image", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images(
            "This is text with no markdown"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
            "This is text with no markdown"
        )
        self.assertListEqual([], matches)

if __name__ == "__main__":
    unittest.main()