from textnode import TextType, TextNode

class HTMLNode ():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props
    
    def to_html(self):
        if self.tag is None:
            return self.value
        
        attrs_html = ""
        for attr, value in self.props.items():
            attrs_html += f' {attr}="{value}"'
        
        if self.tag in self.SELF_CLOSING_TAGS:
            return f"<{self.tag}{attrs_html}/>"
        
        # Check if this is a parent node with no children
        if not self.children:
            # For parent nodes with no children, return an empty element
            return f"<{self.tag}{attrs_html}></{self.tag}>"
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{attrs_html}>{children_html}</{self.tag}>"
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html.rstrip()
          
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None and self.tag == None:
            raise ValueError("All leaf nodes must have either a tag or a value")
        elif self.tag == None:
            return self.value
        elif self.value == None:
            # Self-closing tag
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if children is None:
            children = []
        super().__init__(tag, None, children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a tag")
        elif self.children == []:
            raise ValueError("All parent nodes must have children")
        children_html = ""
        for child in self.children:
            if not hasattr(child, 'to_html') or not callable(child.to_html):
                raise TypeError(f"Child node must be an HTMLNode or compatible type. Found: {type(child)}")
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value=None, props={"src": text_node.url})
    else:
        raise ValueError("Invalid text node type")

