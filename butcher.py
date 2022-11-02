"""Main script"""
import re
from venv import create
from tree_sitter import Language, Parser
from fuzzywuzzy import fuzz,process

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

type_s = ["int", "float", "double", "boolean", "bool", "string", "String","class","public","void"]

operators_list = [["==", "!=", ">=", "<=", ">", "<"],  # comparison
             ["++", "+=", "+", "--", "-=", "-", "//",
                 "/=", "/", "%=", "%", "**", "*=", "*"],
             # arithmetic and assignment
             ["&&", "||", "!", "and", "or", "not"],  # logical
             ["is not", "is"],  # identity
             ["not in", "in"]  # membership
             ]


def create_parse_tree(input_code, input_language):
    """return s-expression and parse tree for the given code and language using the tree-sitter"""
    if input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8"))
    if input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8"))
    return parser_py.parse(bytes(input_code, "utf-8"))


def read_in_file(file_name):
    """reads in file and returns lines in array"""
    with open(file_name, mode="r+", encoding="utf-8") as ground_file:
        lines = ground_file.readlines()
    return lines

def check_equivalence_snippet_ratio(final_string_one, final_string_two):
    """checks fuzz ratio of passed code snippets"""
    return fuzz.ratio(final_string_one,final_string_two)

def get_snippet(string, language):
    """returns a tree sitter snippet for comparison"""
    code_snippet = string
    tree = create_parse_tree(code_snippet,language)
    cursor = tree.walk()
    cursor.goto_first_child()
    final = str(cursor.node.type) + "," + extract_type_(string) + "," + extract_value(string)[0]
    return final

def check_completeness(lines, language):
    line = lines[0]
    tree = create_parse_tree(line,language)
    i = 1
    while ["ERROR","MISSING"] in tree.root_node.sexp() or line == '':
        new_line = lines[i]
        line = line + "\n" + new_line
        tree = create_parse_tree(line,language)
        i += 1
    return line

def extract_type_(input_string):
    """return the type_ of variable if present, derive it otherwise"""
    string = input_string.split()
    for type_ in type_s:
        if type_ in string:
            return type_

    numbers = extract_value(input_string)
    if numbers and len(numbers) == 1:
        if numbers[0][0] in ["true", "false", "True", "False"]:
            return "bool"
        if re.search(r"\.", numbers[0][0]) is None:
            return "int"
        if len(numbers[0][0]) < 9:
            return "float"  # 6-7 significant digits
        return "double"  # 15-16 significant digits

    if numbers:  # more than one extracted value
        flag_float, flag_double = False, False
        for number in numbers:
            if number in ["true", "false", "True", "False"]:
                return "bool"
            if re.search(r"\.", number[0]) is None:
                continue  # int
            if len(number[0]) < 9:
                flag_float = True  # 6-7 significant digits
            else:
                flag_double = True  # 15-16 significant digits
        if flag_double:
            return "double"
        return "float" if flag_float else "int"
    return "string"

def extract_value(input_string):
    """return the values from given input"""
    numbers = re.findall(r'true|false|True|False', input_string)
    string = re.sub('([a-zA-Z]+[_a-zA-Z0-9]*)', '', input_string)
    numbers.extend(re.findall(r'\d+(?:\.\d+)?', string))

    return [number for number in numbers] if numbers else None


def extract_name(input_string):
    """return variable names from given input"""
    string = re.sub('true|false|True|False', '', input_string)
    string = re.sub(r'\(([^\()]*)\)', '@', string) # print argument in java and python
    string = re.sub(r'(?<=<<)(.*)(?=;)', '@', string)  # print argument in cpp

    tokens = string.split()

    for token in tokens:
        if token in type_s:
            tokens.remove(token)
        for op_list in operators_list:
            if token in op_list:
                tokens.remove(token)

    string = " ".join(tokens)
    best_match = process.extractOne(string, keywords.keys(), scorer=fuzz.token_set_ratio)
    if best_match[-1] >= 45:
        return True, best_match[0]

    names = re.findall('([a-z,A-Z]+[_]*[a-z,A-Z,0-9]*)*', string)
    return False, [name for name in names if name and name not in type_s]


def extract_operator(input_string):
    """return operators from given input"""
    extracted_operators = []
    for group in operators_list:
        for operator in group:
            if operator in input_string:
                extracted_operators.append(operator)
    return extracted_operators
 


string_py = "a = 5"
string_jv = "a = 5;"
string_cpp = "a = 5;"



print(check_equivalence_snippet_ratio(get_snippet(string_py,PYTHON),get_snippet(string_jv,JAVA)))

