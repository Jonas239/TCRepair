"""Main script"""
import json
from tree_sitter import Language, Parser

Language.build_library(
    'build/my-languages.so',
    [
        '/Users/jonas/Documents/GitHub/tree-sitter-cpp',
        '/Users/jonas/Documents/GitHub/tree-sitter-java',
        '/Users/jonas/Documents/GitHub/tree-sitter-python'
    ]
)

PY_LANGUAGE = Language('build/my-languages.so', 'python')
JV_LANGUAGE = Language('build/my-languages.so', 'java')
CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')

PYTHON = "PYTHON"
JAVA = "JAVA"
CPP = "CPP"

parser_py = Parser()
parser_py.set_language(PY_LANGUAGE)

parser_jv = Parser()
parser_jv.set_language(JV_LANGUAGE)

parser_cpp = Parser()
parser_cpp.set_language(CPP_LANGUAGE)


def open_file(file):
    """opens a file and returns its content as string"""
    with open(file, "r", encoding="utf-8") as f:
        file_ = f.read()
    return file_


def create_parse_tree(input_code, input_language):
    """return the parse tree for the given code and language using tree-sitter"""
    if input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8"))
    if input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8"))
    if input_language == "PYTHON":
        return parser_py.parse(bytes(input_code, "utf-8"))
    


def node_source_to_string(source, node):
    """returns the corresponding code for every node"""
    return bytes(source, "utf8")[node.start_byte:node.end_byte].decode("utf-8")


def traverse_tree(tree, code):
    """function for traversing the tree"""
    cursor = tree.walk()

    reached_root = False
    while reached_root is False:
        yield cursor.node.type, node_source_to_string(code, cursor.node), cursor.node.start_byte, cursor.node.end_byte

        if cursor.goto_first_child():
            continue

        if cursor.goto_next_sibling():
            continue

        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True

            if cursor.goto_next_sibling():
                retracing = False


def create_dict(tree, code, language):
    """returns the final dict to be written to json"""
    code_ = code
    if language == PYTHON:
        tree = create_parse_tree(code_, PYTHON)
    if language == JAVA:
        tree = create_parse_tree(code_, PYTHON)
    if language == CPP:
        tree = create_parse_tree(code_, CPP)
    traverse_tree_ = traverse_tree(tree, code_)
    json_dict = {}
    for node in traverse_tree_:
        key = node[0] + "_" + str(node[2]) + "_" + str(node[3])
        json_dict[key] = node[1]
    return json_dict

def sanitize_dict(dict):
    """sanitizes the dictionary for unnecessary infos"""
    unnecessary_infos =[")","(",":","=","+","-","*","//",";","^","/","\\","[","]", "{","}",".",",","%","comment","module","translation_unit","&","\""]
    for key in list(dict.keys()):
        for string in unnecessary_infos:
            if string in key:
                try:
                    del dict[key]
                except:
                    continue
    return dict

def create_json(array, language):
    """writes array to json"""
    if language == PYTHON:
        file_name = "py_tree.json"
    if language == JAVA:
        file_name = "jv_tree.json"
    if language == CPP:
        file_name = "cpp_tree.json"
    json_obj = json.dumps(array, indent=4)
    with open(file_name, "w", encoding="utf-8") as outfile:
        outfile.write(json_obj)


if __name__ == "__main__":

    code_cpp = open_file("geeks_for_geeks_dataset/cpp/ADD_1_TO_A_GIVEN_NUMBER.cpp")
    code_java = open_file(
        "geeks_for_geeks_dataset/java/ADD_1_TO_A_GIVEN_NUMBER.java")
    code_python = open_file(
        "geeks_for_geeks_dataset/python/ADD_1_TO_A_GIVEN_NUMBER.py")

    tree_cpp = create_parse_tree(code_cpp, CPP)
    tree_java = create_parse_tree(code_java, JAVA)
    tree_python = create_parse_tree(code_python, PYTHON)

    array_cpp = create_dict(tree_cpp, code_cpp, CPP)
    array_java = create_dict(tree_java, code_java, JAVA)
    array_python = create_dict(tree_python, code_python, PYTHON)

    san_array_cpp = sanitize_dict(array_cpp)
    san_array_java = sanitize_dict(array_java)
    san_array_python = sanitize_dict(array_python)
    
    create_json(san_array_cpp, CPP)
    create_json(san_array_java,JAVA)
    create_json(san_array_python, PYTHON)
