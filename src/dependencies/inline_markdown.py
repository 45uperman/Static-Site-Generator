import re
try:
    from dependencies.textnode import TextNode
    from dependencies.htmlnode import LeafNode
except ModuleNotFoundError:
    from textnode import TextNode
    from htmlnode import LeafNode

def text_to_html_nodes(text):
    return list(map(text_node_to_html_node, text_to_text_nodes(text)))

def text_to_text_nodes(text):
    delimiters = {"**": "bold", "`": "code", "*": "italic"}
    new_nodes = [TextNode(text, "text")]
    for delimiter in delimiters:
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, delimiters[delimiter])
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def text_node_to_html_node(text_node):
    supported_types = {"text": None, "bold": "b", "italic": "i", "code": "code", "link": "a", "image": "img"}
    try:
        tag = supported_types[text_node.text_type]
    except(KeyError):
        raise(NotImplementedError(f"{text_node} has an unsupported text type. The supported text types are:\n{supported_types.keys()}"))
    if tag == "a":
        return LeafNode(tag, text_node.text, {"href": text_node.url})
    if tag == "img":
        return LeafNode(tag, "", {"src": text_node.url, "alt": text_node.text})
    return LeafNode(tag, text_node.text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_nodes = []
    for node in old_nodes:
        if node.text_type != "text" or delimiter not in node.text:
            return_nodes.append(node)
            continue
        new_nodes_text = node.text.split(delimiter)
        if len(new_nodes_text) % 2 == 0:
            raise(Exception(f"Invalid Markdown syntax in {node}: Missing closing {delimiter}"))
        for i in range(len(new_nodes_text)):
            if i % 2 != 0:
                if new_nodes_text[i] != "":
                    return_nodes.append(TextNode(new_nodes_text[i], text_type))
            else:
                if new_nodes_text[i] != "":
                    return_nodes.append(TextNode(new_nodes_text[i], "text"))
    return return_nodes

def split_nodes_image(old_nodes):
    return_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            return_nodes.append(node)
            continue
        text = node.text
        image_tups = extract_markdown_images(text)
        if image_tups == []:
            return_nodes.append(node)
            continue
        for image_tup in image_tups:
            split_text = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if split_text[0] != "":
                return_nodes.append(TextNode(split_text[0], "text"))
            return_nodes.append(TextNode(image_tup[0], "image", image_tup[1]))
            text = split_text[1]
        if text != "":
            return_nodes.append(TextNode(text, "text"))
    return return_nodes

def split_nodes_link(old_nodes):
    return_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            return_nodes.append(node)
            continue
        text = node.text
        link_tups = extract_markdown_links(text)
        if link_tups == []:
            return_nodes.append(node)
            continue
        for link_tup in link_tups:
            split_text = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            if split_text[0] != "":
                return_nodes.append(TextNode(split_text[0], "text"))
            return_nodes.append(TextNode(link_tup[0], "link", link_tup[1]))
            text = split_text[1]
        if text != "":
            return_nodes.append(TextNode(text, "text"))
    return return_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

