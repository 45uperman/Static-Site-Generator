import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    def test_types(self):
        node1 = TextNode("This is an italic text node", "italic")
        node2 = TextNode("This is a code text node", "code")
        node3 = TextNode("This is a bold text node", "bold")
        node4 = TextNode("This is a normal text node", "text")
        self.assertEqual(node1.text_type, "italic")
        self.assertEqual(node2.text_type, "code")
        self.assertEqual(node3.text_type, "bold")
        self.assertEqual(node4.text_type, "text")
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
        self.assertNotEqual(node2, node4)


if __name__ == "__main__":
    unittest.main()
