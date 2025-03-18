import re
from textnode import TextNode, TextType, BlockType
from htmlnode import LeafNode, ParentNode, text_node_to_html_node, HTMLNode

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
    nodes = []
    remaining_text = text
    
    while remaining_text:
        # Find the position of each marker, -1 if not found
        bold_double_asterisk = remaining_text.find("**")
        bold_double_underscore = remaining_text.find("__")
        italic_asterisk = remaining_text.find("*")
        italic_underscore = remaining_text.find("_")
        
        # Set invalid positions to a large number
        if bold_double_asterisk == -1: bold_double_asterisk = float('inf')
        if bold_double_underscore == -1: bold_double_underscore = float('inf')
        if italic_asterisk == -1: italic_asterisk = float('inf')
        if italic_underscore == -1: italic_underscore = float('inf')
        
        # Find the earliest marker
        earliest_marker = min(bold_double_asterisk, bold_double_underscore, 
                              italic_asterisk, italic_underscore)
        
        # If no markers found, add remaining text and break
        if earliest_marker == float('inf'):
            nodes.append(TextNode(remaining_text, TextType.TEXT))
            break
            
        # Add any text before the marker
        if earliest_marker > 0:
            nodes.append(TextNode(remaining_text[:earliest_marker], TextType.TEXT))
            
        # Handle the appropriate marker type
        if earliest_marker == bold_double_asterisk:
            end = remaining_text.find("**", bold_double_asterisk + 2)
            if end != -1:
                nodes.append(TextNode(remaining_text[bold_double_asterisk + 2:end], TextType.BOLD))
                remaining_text = remaining_text[end + 2:]  # Update remaining_text to skip past this marker
            else:
                 # If no closing marker, treat the opening marker as plain text and advance past it
                nodes.append(TextNode(remaining_text[:bold_double_asterisk + 2], TextType.TEXT))
                remaining_text = remaining_text[bold_double_asterisk + 2:]
        elif earliest_marker == bold_double_underscore:
            end = remaining_text.find("__", bold_double_underscore + 2)
            if end != -1:
                nodes.append(TextNode(remaining_text[bold_double_underscore + 2:end], TextType.BOLD))
                remaining_text = remaining_text[end + 2:]
            else:
                nodes.append(TextNode(remaining_text[:bold_double_underscore + 2], TextType.TEXT))
                remaining_text = remaining_text[bold_double_underscore + 2:]
        elif earliest_marker == italic_asterisk:
            end = remaining_text.find("*", italic_asterisk + 1)
            if end != -1:
                nodes.append(TextNode(remaining_text[italic_asterisk + 1:end], TextType.ITALIC))
                remaining_text = remaining_text[end + 1:]
            else:
                nodes.append(TextNode(remaining_text[:italic_asterisk + 1], TextType.TEXT))
                remaining_text = remaining_text[italic_asterisk + 1:]
        elif earliest_marker == italic_underscore:
            end = remaining_text.find("_", italic_underscore + 1)
            if end != -1:
                nodes.append(TextNode(remaining_text[italic_underscore + 1:end], TextType.ITALIC))
                remaining_text = remaining_text[end + 1:]
            else:
                nodes.append(TextNode(remaining_text[:italic_underscore + 1], TextType.TEXT))
                remaining_text = remaining_text[italic_underscore + 1:]         
    return nodes   

def markdown_to_blocks(markdown):
    # Split markdown into blocks
    blocks = markdown.split("\n\n")
    # Remove whitespace from blocks
    blocks = [block.strip() for block in blocks]
    # Remove empty blocks
    blocks = [block for block in blocks if block]
    # Convert blocks to TextNodes
    return blocks

def block_to_block_type(block):
    # Determine the type of block
    count = 0 # Count the number of hashes
    while count < len(block) and block[count] == "#":
        count += 1
    if count > 6 or (count > 0 and (len(block) <= count or block[count] != " ")):
        return BlockType.PARAGRAPH
    if 1 <= count <= 6 and len(block) > count and block[count] == " ":
        return BlockType.HEADING
    elif block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    # Check every line in a quote block starts with ">"
    elif all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    # Check every line in an unordered list block starts with "- "
    elif all(re.match(r"^- ", line) for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    # Check every line in an ordered list block starts with the number 1 and go down by increments followed by ". "
    elif all(re.match(r"^\d+\. ", line) for line in block.split("\n")):
        return BlockType.ORDERED_LIST
   
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    # Convert markdown to single parent HTMLNode
    blocks = markdown_to_blocks(markdown)
    # Determine the type of block
    block_types = [block_to_block_type(block) for block in blocks]
    # Create an appropriate HTML node based on its type using text_node_to_html_node
    html_nodes = []

    # Process each block individually with its type at the same time
    for block, block_type in zip(blocks[:], block_types):
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(ParentNode("p", text_to_textnodes(block)))

        elif block_type == BlockType.HEADING:
            count = 0
            while count < len(block) and block[count] == "#":
                count += 1
            # Ensure that a missing space doesn't break our function
            html_nodes.append(ParentNode(f"h{count}", text_to_textnodes(block[count+1:].strip())))

        elif block_type == BlockType.IMAGE:
            alt_start = block.index("[") + 1
            alt_end = block.index("]")
            url_start = block.index("(") + 1
            url_end = block.index(")")

            alt_text = block[alt_start:alt_end].strip()
            url = block[url_start:url_end].strip()

            html_nodes.append(ParentNode("img", [], {"src": url, "alt": alt_text}))
            
        
        elif block_type == BlockType.CODE:
            # treat block as raw text and wrap it with <code> and <pre> tags
            html_nodes.append(ParentNode("pre", [ParentNode("code", [TextNode(block[3:-3].strip(), TextType.CODE)])]))


        elif block_type == BlockType.QUOTE:
            html_nodes.append(ParentNode("blockquote", text_to_textnodes(block)))

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            items = [item.lstrip() for item in items]
            items = [ParentNode("li", text_to_textnodes(item)) for item in items]
            html_nodes.append(ParentNode("ul", items))

        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n") # Split the block into lines
            list_items = []
            for item in items:
                parts = item.split(".", 1) #Split at the first dot
                if len(parts) > 1: # Ensure there is a nubmer and content
                    content = parts[1].strip() #Extract the part after the dot
                    list_items.append(ParentNode("li", text_to_textnodes(content)))
            html_nodes.append(ParentNode("ol", list_items))
          
    # wrap all nodes into a single parent <div> node
    return ParentNode("div", html_nodes)

def extract_title(markdown):
    # Split the markdown into lines
    lines = markdown.split("\n")
    
    # Look for a line that starts with a single #
    for line in lines:
        if line.startswith("# "):
            # Return the title with the # and any whitespace removed
            return line[2:].strip()
    
    # If we get here, no title was found
    raise ValueError("No title found in markdown")

    
    

    
   










   
