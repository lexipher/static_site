from textnode import TextNode, TextType

def main():
    my_node = TextNode("hello world", TextType.LINK, "https://www.boot.dev")
    print(my_node)

main()