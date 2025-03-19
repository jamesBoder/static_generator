import os
import shutil
from textnode import TextNode, TextType
from code_func import extract_title, markdown_to_html_node

static = './static'
public = './public'
content = './content/index.md'
template = './template.html'
public_index = './public/index.html'
content_dir = './content'  # Directory path



def copy_files(src_dir, dest_dir):
    try:
        # Ensure the source directory exists
        if not os.path.exists(src_dir):
            print(f"Source directory '{src_dir}' does not exist.")
            return
        
        # Ensure the destination directory exists, create if not
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # Iterate over all files in the source directory
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dest_path = os.path.join(dest_dir, item)
            
            # Check if it's a file and copy it
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dest_path)
                print(f"Copied '{src_path}' to '{dest_path}'")
            elif os.path.isdir(src_path):
                copy_files(src_path, dest_path)
            else:
                print(f"Skipped '{src_path}' (not a regular file or directory).")
        
        print("All files copied successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_page(src_path, template_path, dest_path):
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")
    
    # Read markdown file at src_path
    with open(src_path, 'r') as f:
        markdown_content = f.read()

    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Check if the file is empty
    if not markdown_content.strip():
        print(f"Warning: {src_path} is empty")
        # Create a simple placeholder content
        html_content = "<div>No content available</div>"
        title = "Empty Page"
    else:
        # Extract title
        title = extract_title(markdown_content)
        
        # Convert markdown to HTML
        html_node = markdown_to_html_node(markdown_content)

        # Generate HTML content
        try:
            html_content = html_node.to_html()
        except ValueError as e:
            print(f"Error processing {src_path}: {e}")
            html_content = "<div>Error processing content</div>"

    # Replace placeholders in template
    final_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    # Create destination directory if needed
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Ensure the content directory exists
    if not os.path.exists(dir_path_content):
        print(f"Content directory '{dir_path_content}' does not exist.")
        return

    # Create the destination directory if it doesn't exist
    os.makedirs(dest_dir_path, exist_ok=True)

    # Iterate over all files and directories in the content directory
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(src_path) and src_path.endswith('.md'):
            # For a markdown file, create a corresponding HTML file
            # Get the relative path within the content directory
            relative_path = os.path.relpath(src_path, dir_path_content)
            # Create the destination path with .html extension
            html_filename = os.path.splitext(relative_path)[0] + '.html'
            dest_path = os.path.join(dest_dir_path, html_filename)
            
            # Ensure the parent directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            
            # Generate the HTML page
            generate_page(src_path, template_path, dest_path)
        
        elif os.path.isdir(src_path):
            # For a directory, recursively process it
            sub_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, sub_dest_dir)
    

def main():
    
    # Delete all files in public directory
    if os.path.exists(public):
        # Remove the entire directory and recreate it
        shutil.rmtree(public)
        os.makedirs(public)
        print(f"Recreated {public} directory")
    else:
        os.makedirs(public)
        print(f"Created {public} directory")


    copy_files(static, public)
    generate_pages_recursive(content_dir, template, public)
    # text_node = TextNode("this is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node)
    
if __name__ == "__main__":
    main()