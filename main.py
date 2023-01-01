"""Import the tree-sitter parser and the python bindings"""
import json
import os
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

PY_LANGUAGE = Language('build/my-languages.so', 'python')
JV_LANGUAGE = Language('build/my-languages.so', 'java')
CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')

CPP = "CPP"
PYTHON = "PYTHON"
JAVA = "JAVA"

# Create Parsers for the three languages
parser_py = Parser()
parser_py.set_language(PY_LANGUAGE)

parser_jv = Parser()
parser_jv.set_language(JV_LANGUAGE)

parser_cpp = Parser()
parser_cpp.set_language(CPP_LANGUAGE)

class TreeNode:
    """class for accessing tree sitter nodes more easily"""

    def __init__(self, node_type, source_code):
        """Constructor"""
        self.node_type = node_type
        self.source_code = source_code.decode()
        self.children = []

    def print_tree(self, level=0):
        """print the whole tree"""
        print('  ' * level +
              f"Type: {self.node_type} Code: {self.source_code}")
        for child in self.children:
            child.print_tree(level + 1)

    def get_node_type(self):
        """returns the type of a node"""
        return self.node_type

    def get_soure_code(self):
        """returns the corresponding source code for the node"""
        return self.source_code

    def get_children(self):
        """returns all children of a node"""
        return self.children


def tree_sitter_to_tree(node):
    """convert a tree sitter tree to a TreeNode tree, requires the root node to be passed"""
    tree_node = TreeNode(node.type, node.text)
    for i in range(node.child_count):
        child = node.children[i]
        tree_node.children.append(tree_sitter_to_tree(child))

    return tree_node

def find_best_fit(root, code_string):
    """finds the fitting node type for given source code"""
    if root.source_code == code_string:
        return (root.source_code, root.node_type)
    for child in root.children:
        result = find_best_fit(child, code_string)
        if result is not None:
            return result
    return None

def tokenize(src_code, language):
    parser = Parser()
    parser.set_language(language)
    tree = parser.parse(src_code)
    tokens = []
    for node in tree.iter_tokens():
        tokens.append(node.utf8_text())
    return tokens


def create_parse_tree(input_code, input_language):
    """return s-expression and parse tree for the given code and language using the tree-sitter"""
    if input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8")).root_node
    if input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8")).root_node
    if input_language == "PYTHON":
        return parser_py.parse(bytes(input_code, "utf-8")).root_node


def return_file_content(file_path):
    """returns file content"""
    with open(file_path, "r+", encoding='utf-8') as f:
        file = f.read()
    return file


python_file = return_file_content("self_made_dataset/python/two_functions.py")
java_file = return_file_content("self_made_dataset/java/assignment.java")
cpp_file = return_file_content("self_made_dataset/cpp/assignment.cpp")

python_root_node = create_parse_tree(python_file, PYTHON)
java_root_node = create_parse_tree(java_file, JAVA)
cpp_root_node = create_parse_tree(cpp_file, CPP)

python_tree = tree_sitter_to_tree(python_root_node)
java_tree = tree_sitter_to_tree(java_root_node)
cpp_tree = tree_sitter_to_tree(cpp_root_node)

code = """
def add(x, y):
    return x + y
"""

tokens = tokenize(code, PY_LANGUAGE)
print(tokens)





# python_tree.print_tree()
# replace_tokens(python_tree, "self_made_dataset/python/two_functions.py", "rule-set-python.json")
# replace_tokens(java_tree, "self_made_dataset/java/two_functions.java", "rule-set-java.json")
# replace_tokens(cpp_tree, "self_made_dataset/cpp/two_functions.cpp", "rule-set-cpp.json")


# print("------------------------------------------------PYTHON------------------------------------------------")
# python_tree = tree_sitter_to_tree(python_root_node)
# python_tree.print_tree()
# print(" ")
# print("------------------------------------------------JAVA------------------------------------------------")
# java_tree = tree_sitter_to_tree(java_root_node)
# java_tree.print_tree()
# print(" ")
# print("------------------------------------------------CPP------------------------------------------------")
# cpp_tree = tree_sitter_to_tree(cpp_root_node)
# cpp_tree.print_tree()
