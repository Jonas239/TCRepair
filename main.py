"""Import the tree-sitter parser and the python bindings"""
import json
import os
from tree_sitter import Language, Parser

Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',

    # Include one or more languages
    [
        '/Users/jonas/tree-sitter-python',
        '/Users/jonas/tree-sitter-java',
        '/Users/jonas/tree-sitter-cpp'
    ]
)

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


# def tree_sitter_to_tree(node):
#     """convert a tree sitter tree to a TreeNode tree, requires the root node to be passed"""
#     tree_node = TreeNode(node.type, node.text)
#     for i in range(node.child_count):
#         child = node.children[i]
#         tree_node.children.append(tree_sitter_to_tree(child))

#     return tree_node

def load_node_type_mapping():
    with open("node_type_mapping.json", "r") as f:
        return json.load(f)

def get_language(file):
    if file.endswith(".py"):
        return PYTHON
    elif file.endswith(".java"):
        return JAVA
    elif file.endswith(".cpp"):
        return CPP
    else:
        return None

def parse_file(file):
    with open(file, "r") as f:
        code = f.read()
        if get_language(file) == PYTHON:
            return parser_py.parse(bytes(code, 'utf8'))
        elif get_language(file) == JAVA:
            return parser_jv.parse(bytes(code, 'utf8'))
        elif get_language(file) == CPP:
            return parser_cpp.parse(bytes(code, 'utf8'))
        else:
            return None

def map_node_type(node_type, to_language, node_type_mapping):
    if node_type in node_type_mapping:
        return node_type_mapping[node_type][to_language]
    return None

def get_key_from_value(value, language, node_type_mapping):
    for key, val in node_type_mapping.items():
        if val[language] == value:
            return key
    return None

def translate_node_type(node_type, from_language, to_language, node_type_mapping):
    key = get_key_from_value(node_type, from_language, node_type_mapping)
    return map_node_type(key, to_language, node_type_mapping)

def split_text(text):
    return text.split(" ")

def find_best_fit(root, code_string):
    """finds the fitting node type for given source code"""
    if root.source_code == code_string:
        return (root.source_code, root.node_type)
    for child in root.children:
        result = find_best_fit(child, code_string)
        if result is not None:
            return result
    return None

def tree_sitter_to_tree(node, node_type_mapping, from_language, to_language):
    """convert a tree sitter tree to a TreeNode tree, requires the root node to be passed"""
    tree_node = TreeNode(translate_node_type(node.type, from_language, to_language, node_type_mapping), node.text)
    for i in range(node.child_count):
        child = node.children[i]
        tree_node.children.append(tree_sitter_to_tree(child, node_type_mapping, from_language, to_language))

    return tree_node

def ask_user_for_node_type(node_type, from_language, to_language, node_type_mapping):
    print(f"Please enter the node type for {node_type} in {to_language}:")
    new_node_type = input()
    node_type_mapping[node_type] = {from_language: node_type, to_language: new_node_type}
    return new_node_type










