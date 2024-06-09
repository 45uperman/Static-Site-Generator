try:
    from dependencies.htmlnode import ParentNode
    from dependencies.inline_markdown import text_to_html_nodes
except ModuleNotFoundError:
    from htmlnode import ParentNode
    from inline_markdown import text_to_html_nodes

class BlockType():
    heading = ["null_heading", "h1", "h2", "h3", "h4", "h5", "h6"]
    code = "code"
    quote = "blockquote"
    unordered_list = "ul"
    ordered_list = "ol"
    paragraph = "p"

def markdown_to_blocks(markdown):
    rough_blocks = markdown.split("\n\n")
    strip_block = lambda rough_block: rough_block.strip()
    block_not_empty = lambda clean_block: clean_block.replace("\n", "") != ""
    clean_blocks = map(strip_block, rough_blocks)
    return list(filter(block_not_empty, clean_blocks))

def block_to_block_type(block):
    if block.startswith("#") and (" " in block[:7]):
        h=0
        for char in block:
            if char != "#":
                break
            h += 1
        return BlockType.heading[h]
    elif block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.code
    elif block.startswith(">"):
        quote = True
        for line in block.split("\n"):
            if line.startswith(">") is False:
                quote = False
                break
        if quote:
            return BlockType.quote
    elif block.startswith("* ") or block.startswith("- "):
        unordered_list = True
        for line in block.split("\n"):
            if (line.startswith("* ") or line.startswith("- ")) is False:
                unordered_list = False
                break
        if unordered_list:
            return BlockType.unordered_list
    elif block.startswith("1. "):
        ordered_list = True
        i = 1
        for line in block.split("\n"):
            if line.startswith(f"{i}. ") is False:
                ordered_list = False
                break
            i += 1
        if ordered_list:
            return BlockType.ordered_list
    else:
        return BlockType.paragraph

def block_to_htmlnode(block):
    block_type = block_to_block_type(block)
    if block_type in BlockType.heading:
        children = text_to_html_nodes(block.lstrip("#").strip())
        return ParentNode(block_type, children)
    elif block_type == BlockType.code:
        children = text_to_html_nodes(block[4:-4])
        return ParentNode("pre", [ParentNode(block_type, children)])
    elif block_type == BlockType.quote:
        children = text_to_html_nodes(" ".join(list(map(lambda line: line.lstrip(">").strip(), block.split("\n")))))
        return ParentNode(block_type, children)
    elif block_type == BlockType.unordered_list:
        children = list(map(lambda line: ParentNode("li", text_to_html_nodes(line[2:].strip())), block.split("\n")))
        return ParentNode(block_type, children)
    elif block_type == BlockType.ordered_list:
        children = list(map(lambda line: ParentNode("li", text_to_html_nodes(line[3:].strip())), block.split("\n")))
        return ParentNode(block_type, children)
    else:
        children = text_to_html_nodes(" ".join(map(lambda line: line.strip(), block.split("\n"))))
        return ParentNode(block_type, children)
    
def markdown_to_html_node(markdown):
    html_blocks = list(map(block_to_htmlnode, markdown_to_blocks(markdown)))
    return ParentNode("div", html_blocks)
