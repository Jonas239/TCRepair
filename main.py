# Import the tree-sitter parser and the python bindings
from tree_sitter import Language, Parser

Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',

    # Include one or more languages
    [
        '/tree-sitter-python',
        '/tree-sitter-java',
        '/tree-sitter-cpp'
    ]
)

PY_LANGUAGE = Language('build/my-languages.so', 'python')
JV_LANGUAGE = Language('build/my-languages.so', 'java')
CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')

parser = Parser()
parser.set_language(PY_LANGUAGE)
tree = parser.parse(bytes("""
def foo():
    if bar:
        baz()
""", "utf8"))

# Create a tree-sitter parser object for the desired language

# Convert the tree-sitter parser to a tree-sitter syntax tree

# Get the root node of the tree
root_node = tree.root_node

# Define a Python tree node class


class TreeNode:
    def __init__(self, type, text):
        self.type = type
        self.text = text
        self.children = []

    def print_tree(self, level=0):
        # Print the current node's type and text, indented according to its level in the tree
        print('  ' * level + f"Type: {self.type}, Text: {self.text}")

        # Recursively print the children of the node
        for child in self.children:
            child.print_tree(level + 1)

# Traverse the tree-sitter tree and add its nodes to a Python tree


def traverse_tree(node):
    # Create a Python tree node for the current tree-sitter node
    tree_node = TreeNode(node.type, node.text)

    # Recursively traverse the children of the node and add them to the Python tree
    for i in range(node.child_count):
        child = node.children[i]
        tree_node.children.append(traverse_tree(child))

    return tree_node


python_tree = traverse_tree(root_node)
python_tree.print_tree()
