import os
import shutil
from textnode import TextNode, TextType
from code_func import extract_title, markdown_to_html_node

static = './static'
public = './public'
content = './content/index.md'
template = './template.html'
public_index = './public/index.html'


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
    # Read markdown file at src_path and store in variable
    with open(src_path, 'r') as f:
        markdown_content = f.read()

    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown_content)

    # Replace placeholders in template
    final_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    # Create destination directory if needed
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(final_html)


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
    generate_page(content, template, public_index)
    # text_node = TextNode("this is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node)

if __name__ == "__main__":
    main()