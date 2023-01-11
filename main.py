"""Import the tree-sitter parser and the python bindings"""
import json
from tree_sitter import Language, Parser
from fuzzywuzzy import fuzz

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

languages = [PYTHON, JAVA, CPP]

# Create Parsers for the three languages
parser_py = Parser()
parser_py.set_language(PY_LANGUAGE)

parser_jv = Parser()
parser_jv.set_language(JV_LANGUAGE)

parser_cpp = Parser()
parser_cpp.set_language(CPP_LANGUAGE)


class TreeNode:
    def __init__(self, node_type, source_code, language_specific_type):
        self.node_type = node_type
        self.source_code = source_code.decode()
        self.children = []
        self.language_specific_type = language_specific_type

    def print_tree(self, level=0):
        print('  ' * level + f"Lifted Type: {self.node_type} , Original Type: {self.language_specific_type} , Code: {self.source_code}")
        for child in self.children:
            child.print_tree(level + 1)
            
    def get_node_type(self):
        return self.node_type

    def get_source_code(self):
        return self.source_code

    def get_children(self):
        return self.children

    def get_all_function_heads(self):
        function_heads = []
        if self.node_type == "function_definition":
            function_heads.append(self)
        for child in self.children:
            function_heads.extend(child.get_all_function_heads())
        return function_heads

    def get_function_body(self):
        function_body = []
        if self.node_type == "function_body":
            function_body.append(self)
        for child in self.children:
            function_body.extend(child.get_function_body())
        return function_body

    def get_all_function_bodies_with_heads_as_key(self):
        function_bodies = {}
        if self.node_type == "function_definition":
            function_bodies[self] = self.get_function_body()
        for child in self.children:
            function_bodies.update(child.get_all_function_bodies_with_keys_as_key())
        return function_bodies

    def filter_for_node_type(self, node_type):
        filtered_nodes = []
        if self.language_specific_type == node_type:
            filtered_nodes.append(self.source_code)
        for child in self.children:
            filtered_nodes.extend(child.filter_for_node_type(node_type))
        return filtered_nodes




# def tree_sitter_to_tree(node):
#     """convert a tree sitter tree to a TreeNode tree, requires the root node to be passed"""
#     tree_node = TreeNode(node.type, node.text)
#     for i in range(node.child_count):
#         child = node.children[i]
#         tree_node.children.append(tree_sitter_to_tree(child))

#     return tree_node

def load_node_type_mapping():
    """loads the node type mapping from a json file"""
    with open("node_type_mapping.json", "r", encoding="utf-8") as file:
        return json.load(file)

def write_to_json_file(node_type_mapping, filepath):
    with open(filepath, "w") as f:
        json.dump(node_type_mapping, f)

def parse_file(file, language):
    """parses a file and returns the root node"""
    with open(file, "r", encoding="utf-8") as file_new:
        code = file_new.read()
        if language == PYTHON:
            return parser_py.parse(bytes(code, 'utf8'))
        if language == JAVA:
            return parser_jv.parse(bytes(code, 'utf8'))
        if language == CPP:
            return parser_cpp.parse(bytes(code, 'utf8'))
        return None


def map_node_type(node_type, to_language, node_type_mapping):
    """maps a node type to another language"""
    if node_type in node_type_mapping:
        return node_type_mapping[node_type][to_language]
    return None


# def get_key_from_value(value, language, node_type_mapping):
#     """returns the key for a given value"""
#     for key, val in node_type_mapping.items():
#         if val[language] == value:
#             return key
#     return None


def get_keys_from_value(value, language, node_type_mapping_):
    """returns the keys for a given value"""
    return [key for key, val in node_type_mapping_.items() if val[language] == value]

# def get_keys_from_value(value, language, node_type_mapping_):
#     """returns the keys for a given value"""
#     keys = [key for key, val in node_type_mapping_.items() if val.get(language, None) == value]
#     if not keys:
#         raise KeyError(f'No keys found for value {value} in language {language}')
#     return keys


def translate_node_type(node_type, from_language, to_language, node_type_mapping):
    """translates a node type from one language to another"""
    key = get_keys_from_value(node_type, from_language, node_type_mapping)
    return map_node_type(key, to_language, node_type_mapping)


def split_text(text):
    """splits a text into a list of words"""
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


def tree_sitter_to_tree(node, node_type_mapping_, from_language):
    """convert a tree sitter tree to a TreeNode tree, requires the root node to be passed"""
    tree_node = TreeNode(get_keys_from_value(node.type, from_language, node_type_mapping), node.text, node.type)
    for i in range(node.child_count):
        child = node.children[i]
        tree_node.children.append(tree_sitter_to_tree(
            child, node_type_mapping_, from_language))

    return tree_node

def check_tree(tree_node, language, node_type_mapping_, languages_):
    """checks if the node type is correct, if not, the user is asked to select the correct node type"""
    if isinstance(tree_node.node_type, list) and len(tree_node.node_type) > 2:
        print("Multiple possible generalized node types found for \nsource code: " + tree_node.source_code + "\nnode type: " + tree_node.language_specific_type + "\n")
        for i, t in enumerate(tree_node.node_type):
            print(f"{i+1}: {t}")
        choice = int(input("Please select a generalized node type (1-{}): ".format(len(tree_node.node_type))))
        tree_node.node_type = tree_node.node_type[choice-1]
    elif isinstance(tree_node.node_type, list) and len(tree_node.node_type) == 1:
        tree_node.node_type = tree_node.node_type[0]
    elif isinstance(tree_node.node_type, list) and len(tree_node.node_type) == 0:
        new_node_type = input("Please enter a generalized node type name for \nsource code: " + tree_node.source_code +  " \nnode type: "+ tree_node.language_specific_type + "\n")
        tree_node.node_type = new_node_type
        node_type_mapping_[new_node_type] = {language: tree_node.language_specific_type}
        for lang in languages_:
            if lang != language:
                if node_type_mapping_[new_node_type][lang]:
                    continue
                else:
                    node_type_mapping_[new_node_type][lang] = None

    for child in tree_node.children:
        check_tree(child, language, node_type_mapping, languages_)

def check_tree_nodes_equal(node1, node2):
    """checks if two trees are equal"""
    node_type_equal = node1.node_type == node2.node_type
    source_code_equal = fuzz.partial_ratio(node1.source_code, node2.source_code)
    equalities = [node_type_equal, source_code_equal]

    if len(node1.children) != len(node2.children):
        return 0.0

    for child1, child2 in zip(node1.children, node2.children):
        equalities.append(check_tree_nodes_equal(child1, child2))

    return sum(equalities) / len(equalities)


python_file = parse_file("self_made_dataset/python/two_functions.py", PYTHON)
java_file = parse_file("self_made_dataset/java/assignment.java", JAVA)
cpp_file = parse_file("self_made_dataset/cpp/assignment.cpp", CPP)

node_type_mapping = load_node_type_mapping()

python_tree = tree_sitter_to_tree(python_file.root_node, node_type_mapping, PYTHON)
# java_tree = tree_sitter_to_tree(java_file.root_node, node_type_mapping, JAVA)
# cpp_tree = tree_sitter_to_tree(cpp_file.root_node, node_type_mapping, CPP)

# check_tree(python_tree, PYTHON, node_type_mapping, languages_=languages)
# check_tree(java_tree, JAVA, node_type_mapping, languages_=languages)
# check_tree(cpp_tree, CPP, node_type_mapping, languages_=languages)


python_tree.print_tree()
print(python_tree.filter_for_node_type('function_definition'))

FILEPATH = "node_type_mapping.json"
write_to_json_file(node_type_mapping, FILEPATH)
