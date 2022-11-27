"""Main script"""
from tree_sitter import Language, Parser
from tree_hugger.core import PythonParser, JavaParser, CPPParser


Language.build_library(
    'build/my-languages.so',
    [
        "/Users/jonas/Documents/GitHub/TCRepair"
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


def create_parser(input_code, input_language):
    """return the parse tree for the given code and language using tree-sitter"""
    if input_language == "CPP":
        return parser_cpp.parse(bytes(input_code, "utf-8"))
    if input_language == "JAVA":
        return parser_jv.parse(bytes(input_code, "utf-8"))
    if input_language == "PYTHON":
        return parser_py.parse(bytes(input_code, "utf-8"))

def create_hugger(language):
    """return a hugger to retrieve all information"""
    if language == PYTHON:
        return PythonParser()
    if language == JAVA:
        return JavaParser()
    if language == CPP:
        return CPPParser()


if __name__ == "__main__":

    py = create_hugger(PYTHON)
    jv = create_hugger(JAVA)
    cpp = create_hugger(CPP)

    py.parse_file("geeks_for_geeks_dataset/python/ADD_1_TO_A_GIVEN_NUMBER_1.python")
    jv.parse_file("geeks_for_geeks_dataset/java/ADD_1_TO_A_GIVEN_NUMBER_1.java")
    cpp.parse_file("geeks_for_geeks_dataset/cpp/ADD_1_TO_A_GIVEN_NUMBER_1.cpp")

    py_function_names = py.get_all_function_names()
    jv_function_names = jv.get_all_class_method_names()
    cpp_function_names = cpp.get_all_function_names()

    print(py_function_names)
    print("--------------------------------------------------------")
    print(jv_function_names)
    print("--------------------------------------------------------")
    print(cpp_function_names)

