try:
    from dependencies.block_markdown import BlockType, markdown_to_html_node
except ModuleNotFoundError:
    from block_markdown import BlockType, markdown_to_html_node

class ConvertableDocument:
    def __init__(self, markdown: str) -> None:
        self.markdown = markdown
        self.htmlnode = markdown_to_html_node(markdown)
        self.html_title = self.__get_title__()
    
    def __get_title__(self):
        blocks = self.htmlnode.children
        found_title = False
        for block in blocks:
            if block.tag == BlockType.heading[1]:
                if found_title is True:
                    raise ValueError(f"Provided markdown has more than one title:\n~~~~~~\n{self.markdown}\n~~~~~~")
                title = block.to_html()
                found_title = True
        if found_title is False:
            raise ValueError(f"Provided markdown is missing a title:\n~~~~~~\n{self.markdown}\n~~~~~~~")
        else:
            return title
    
    def to_html(self):
        return self.htmlnode.to_html()
