import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            delimiter_str = delimiter.text if isinstance(delimiter, TextNode) else delimiter

            if delimiter_str in node.text:
                parts = node.text.split(delimiter)
                
                # If we have an odd number of parts, we found matching pairs of delimiters
                if len(parts) % 2 == 0:
                    # This means a closing delimiter is missing
                    raise ValueError(f"Missing closing delimiter {delimiter} in {node.text}")
                
                # First part is always regular text
                if parts[0]:  # Only add if not empty
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
                # Process remaining parts
                for i in range(1, len(parts)):
                    part = parts[i]
                    # Odd indices (1, 3, 5...) are delimited content
                    if i % 2 == 1:
                        new_nodes.append(TextNode(part, text_type))
                    # Even indices (2, 4, 6...) are regular text
                    else:
                        if part:  # Only add if not empty
                            new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
 # Find all image tags
    image_tags = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    
    return image_tags

def extract_markdown_links(text):
    # Find all link tags (making sure they're not image tags)
    link_tags = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_tags

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            image_tags = extract_markdown_images(node.text)
            if image_tags:
                parts = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
                for i, part in enumerate(parts):
                    if i % 3 == 0:
                        if part:
                            new_nodes.append(TextNode(part, TextType.TEXT))
                    elif i % 3 == 1:
                        new_nodes.append(TextNode(part, TextType.IMAGE))
                    elif i % 3 == 2:
                        new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            link_tags = extract_markdown_links(node.text)
            if link_tags:
                parts = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
                for i, part in enumerate(parts):
                    if i % 3 == 0:
                        if part:
                            new_nodes.append(TextNode(part, TextType.TEXT))
                    elif i % 3 == 1:
                        new_nodes.append(TextNode(part, TextType.LINK))
                    elif i % 3 == 2:
                        new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    # COnvert markdown text into list of TextNodes
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
