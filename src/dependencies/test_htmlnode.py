import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"KEY_ONE": "value_one", "KEY_TWO": "value_two", "KEY_THREE": "value_three"})
        print(node.props_to_html())
    
    def test_print(self):
        node = HTMLNode("This is my tag", "This is my value", "These are my children", {"These": "are", "my": "props"})
        print(node)
    
    def test_leaf_node(self):
        node_1 = LeafNode("a", "boot.dev", {"href": "https://www.boot.dev"})
        node_2 = LeafNode("i", "WOOOOOOOOO")
        node_3 = LeafNode("img", "", {"src": "https://images.everydayhealth.com/images/diet-nutrition/how-many-calories-are-in-a-banana-1440x810.jpg?sfvrsn=be4504bc_1", "alt": "Banana."})
        html_1 = node_1.to_html()
        html_2 = node_2.to_html()
        html_3 = node_3.to_html()
        print(f"***\n{html_1}\n{html_2}\n{html_3}")
    
    def test_parent_node(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                LeafNode("img", "", {"src": "https://images.everydayhealth.com/images/diet-nutrition/how-many-calories-are-in-a-banana-1440x810.jpg?sfvrsn=be4504bc_1", "alt": "Banana."}),
            ],
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode("a", "boot.dev", {"href": "https://www.boot.dev"}),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                node1,
            ],
        )
        node3 = ParentNode(
            "p",
            [
                LeafNode("a", "boot.dev", {"href": "https://www.boot.dev"}),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                node2,
            ],
        )
        node4 = ParentNode("p", [node3])
        print(f"{node4.to_html()}")

if __name__ == "__main__":
    unittest.main()
