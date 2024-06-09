class HTMLNode():
    __void_elements__ = ("area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr")
    def __init__(self, tag=None, value="", children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> NotImplementedError:
        raise NotImplementedError("Use LeafNode or ParentNode objects instead of the parent class HTMLNode")
    
    def props_to_html(self):
        return_string = ""
        for key in self.props:
            return_string += (f' {key}="{self.props[key]}"')
        return return_string
    
    def __repr__(self):
        return f"TAG={self.tag}\nVALUE={self.value}\nCHILDREN={self.children}\nPROPS={self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value: str = "", props={}):
        if type(value) is not str:
            raise TypeError(f"'{type(value)}' object is not a string")
        if not value and tag not in self.__void_elements__:
            raise ValueError("LeafNode object requires a value unless it is a void element")
        super(LeafNode, self).__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.tag is None:
            return self.value
        return_string = f"<{self.tag}{self.props_to_html()}>{self.value}"
        if (self.tag in self.__void_elements__) is False:
            return_string += f"</{self.tag}>"
        return return_string

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props={}):
        if type(tag) is not str:
            raise TypeError(f"'{type(tag)}' object is not a string")
        if type(children) is not list:
            raise TypeError(f"'{type(tag)}' object is not a list")
        if not tag:
            raise ValueError("ParentNode object requires a tag")
        if not children:
            raise ValueError("ParentNode object requires children")
        super().__init__(tag, "", children, props)
    
    def to_html(self) -> str:
        return_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            return_string += child.to_html()
        return return_string + f"</{self.tag}>"
