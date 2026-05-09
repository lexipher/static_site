import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Look at me!")
        self.assertEqual(node.to_html(), '<b>Look at me!</b>')

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


if __name__ == "__main__":
    unittest.main()