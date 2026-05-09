
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None or self.props == "":
            return ""
        html_props = ""
        for key in self.props:
            html_props += " " + key + '="' + self.props[key] + '"'

        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("Missing Value")
        if self.tag == None:
            return self.value

        return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Missing Tag")
        if self.children == None:
            raise ValueError("Missing Children")
        
        html_tag = "<" + self.tag + self.props_to_html() + ">"

        for child in self.children:
            html_tag += child.to_html()
        
        html_tag += "</" + self.tag + ">"

        return html_tag
    
