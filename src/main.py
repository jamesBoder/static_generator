from textnode import TextNode, TextType



def main():
    text_node = TextNode("this is some anchor text", TextType.LINKS, "https://www.boot.dev")
    print(text_node)

if __name__ == "__main__":
    main()