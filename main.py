"""Main script"""
from tree_sitter import Language, Parser
import json

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


def create_parse_tree(input_code, input_language):
    """return the parse tree for the given code and language using tree-sitter"""
    if input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8"))
    if input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8"))
    return parser_py.parse(bytes(input_code, "utf-8"))

def node_text_bytes(source, node):
    return source[node.start_byte:node.end_byte]

def node_text_string(source, node):
    return bytes(source, "utf8")[node.start_byte:node.end_byte].decode("utf-8")

def traverse_tree(tree, code):
    cursor = tree.walk()

    reached_root = False
    while reached_root == False:
        yield cursor.node.type, node_text_string(code, cursor.node), cursor.node.start_byte, cursor.node.end_byte

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

code = "int function(){return a + c;} int another_function {return a + b;}"
tree = create_parse_tree(code,CPP)
traverse_tree = traverse_tree(tree, code)
json_dict = {}
for node in traverse_tree:
    key = node[0] + "_" + str(node[2]) + "_" + str(node[3])
    json_dict[key] = node[1]


json_obj = json.dumps(json_dict,indent=4)
with open("py_tree.json","w") as outfile:
    outfile.write(json_obj)












