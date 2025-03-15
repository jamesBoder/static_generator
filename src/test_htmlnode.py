import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import TextType, TextNode
from htmlnode import text_node_to_html_node
from code_func import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div", None, {"class": "container"})
        self.assertEqual(node.props_to_html(), ' class="container"')

    def test_props_to_html_empty(self):
        node = HTMLNode("div", "This is a div", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("div", "This is a div", None, {"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(div, This is a div, None, {'class': 'container'})")

    def test_repr_empty(self):
        node = HTMLNode("div", "This is a div", None, None)
        self.assertEqual(repr(node), "HTMLNode(div, This is a div, None, None)")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click me</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "HTMLNode(p, Hello, world!, None, None)")

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

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_repr_parent_node(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(repr(parent_node), "HTMLNode(div, None, [], None)")

    def test_repr_leaf_node(self):
        leaf_node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(leaf_node), "HTMLNode(p, Hello, world!, None, None)")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):      
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node") 

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):   
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/image.jpg"})    

    def test_split_nodes_delimiter(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        node3 = TextNode("This is an italic node", TextType.ITALIC)
        nodes = [node1, node2, node3]
        delimiter = TextNode("This is a bold node", TextType.BOLD)
        text_type = TextType.BOLD
        new_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(new_nodes, [node1, node2, node3])

    def test_split_nodes_delimiter_with_delimiter(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        node3 = TextNode("This is an italic node", TextType.ITALIC)
        nodes = [node1, node2, node3]
        delimiter = TextNode("This is a bold node", TextType.BOLD)
        text_type = TextType.BOLD
        new_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(new_nodes, [node1, node2, node3])

    def test_split_nodes_delimiter_with_delimiter_in_text(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        node3 = TextNode("This is an italic node", TextType.ITALIC)
        nodes = [node1, node2, node3]
        delimiter = TextNode("bold", TextType.TEXT)
        text_type = TextType.BOLD
        new_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(new_nodes, [node1, TextNode("This is a bold node", TextType.BOLD), node3])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_nodes_image(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev/image.jpg")
        node3 = TextNode("This is a text node", TextType.TEXT)
        nodes = [node1, node2, node3]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes, [node1, node2, node3])

    def test_split_nodes_image_with_image(self):
        node1 = TextNode("This is a text node", TextType.TEXT)  
        node2 = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev/image.jpg")
        node3 = TextNode("This is a text node", TextType.TEXT)
        nodes = [node1, node2, node3]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes, [node1, node2, node3])

    def test_text_to_textnodes(self):
        text = "This is a text node"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(text_nodes, [TextNode("This is a text node", TextType.TEXT)])

    def test_markdown_to_blocks(self):
        markdown = "This is a text node"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [TextNode("This is a text node", TextType.TEXT)])

 
        

            
    




if __name__ == "__main__":
    unittest.main()