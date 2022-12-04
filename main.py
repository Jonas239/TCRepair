"""Main script"""
import statistics
import re
from tree_hugger.core import PythonParser, JavaParser, CPPParser
from fuzzywuzzy import fuzz, process

PYTHON = "PYTHON"
JAVA = "JAVA"
CPP = "CPP"

types = ["int", "float", "double", "boolean", "bool",
         "string", "String", "class", "public", "void"]

operators = [["==", "!=", ">=", "<=", ">", "<"],  # comparison
             ["++", "+=", "+", "--", "-=", "-", "//",
                 "/=", "/", "%=", "%", "**", "*=", "*"],
             # arithmetic and assignment
             ["&&", "||", "!", "and", "or", "not"],  # logical
             ["is not", "is"],  # identity
             ["not in", "in"]  # membership
             ]


def open_file(file):
    """opens a file and returns its content as string"""
    with open(file, "r", encoding="utf-8") as f:
        file_ = f.read()
    return file_


def create_hugger(language):
    """return a hugger to retrieve all information"""
    if language == PYTHON:
        return PythonParser(library_loc="build/my-languages.so")
    if language == JAVA:
        return JavaParser(library_loc="build/my-languages.so")
    if language == CPP:
        return CPPParser(library_loc="build/my-languages.so")


# def get_function_heads(py, jv, cpp):
#     if py:
#         return py.get_all_function_names_with_params()
#     if jv:
#         return jv.get_all_method_names_with_params()
#     if cpp:
#         return cpp.get_all_function_names_with_params()


# def get_function_bodies(language):
#     if language == PYTHON:
#         return py.get_all_function_bodies()
#     if language == JAVA:
#         return jv.get_all_class_method_bodies()
#     if language
#         return cpp.get_all_function_bodies()

def erase_none_values(a_tuple):
    """erase none values from parameter list"""
    res = list(a_tuple)
    check = []
    for item in res:
        if item is not None:
            check.append(item)
    return check


def compare_function_heads(language_one, language_two, py_=None, jv_=None, cpp_=None):
    """compares the heads of two functions and gives an estimate on equality"""
    py, jv, cpp = py_, jv_, cpp_
    findings = {}
    sums = []

    if language_one == PYTHON and language_two == JAVA or language_one == JAVA and language_two == PYTHON:
        if py and jv:
            for py_key, jv_key in zip(py.keys(), jv.keys()):
                if py_key == jv_key:
                    py_params = py[py_key]
                    jv_params = jv[jv_key]
                    for py_s_params, jv_s_params in zip(py_params, jv_params):
                        final_compare_py = erase_none_values(py_s_params)
                        final_compare_jv = erase_none_values(jv_s_params)
                        print(final_compare_py)
                        print(final_compare_jv)
                        for item, jitem in zip(final_compare_py, final_compare_jv):
                            sums.append(fuzz.ratio(item, jitem))
                        findings[py_key] = statistics.median(sums)

    if language_one == PYTHON and language_two == CPP or language_one == CPP and language_two == PYTHON:
        if py and cpp:
            for py_key, cpp_key in zip(py.keys(), cpp.keys()):
                if py_key == cpp_key:
                    py_params = py[py_key]
                    cpp_params = cpp[cpp_key]
                    for py_s_params, cpp_s_params in zip(py_params, cpp_params):
                        final_compare_py = erase_none_values(py_s_params)
                        final_compare_cpp = erase_none_values(cpp_s_params)
                        for item, jitem in zip(final_compare_py, final_compare_cpp):
                            sums.append(fuzz.ratio(item, jitem))
                        findings[py_key] = statistics.median(sums)

    if language_one == JAVA and language_two == CPP or language_one == CPP and language_two == JAVA:
        if jv and cpp:
            for cpp_key, jv_key in zip(cpp.keys(), jv.keys()):
                if cpp_key == jv_key:
                    cpp_params = cpp[cpp_key]
                    jv_params = jv[jv_key]
                    for cpp_s_params, jv_s_params in zip(cpp_params, jv_params):
                        final_compare_cpp = erase_none_values(cpp_s_params)
                        final_compare_jv = erase_none_values(jv_s_params)
                        for item, jitem in zip(final_compare_cpp, final_compare_jv):
                            sums.append(fuzz.ratio(item, jitem))
                        findings[cpp_key] = statistics.median(sums)
    return findings


def compare_function_bodies(language_one, language_two, py_=None, jv_=None, cpp_=None):
    """compares the bodies of two functions and gives an estimate on equality"""
    py, jv, cpp = py_, jv_, cpp_
    findings = {}
    sums = []

    if language_one == PYTHON and language_two == JAVA or language_one == JAVA and language_two == PYTHON:
        if py and jv:
            for key_py, key_jv in zip(py.keys(), jv.keys()):
                python_body = py[key_py]
                java_body = jv[key_jv]
                python_body_splitted = sanitize_python_body(python_body)
                java_body_splitted = sanitize_java_cpp_body(java_body)
                print(python_body_splitted)
                print(java_body_splitted)
                for python_line, java_line in zip(python_body_splitted, java_body_splitted):
                    print(python_line)
                    print(java_line)
                    sums.append(compare_line(python_line, java_line))
                findings[key_py] = statistics.median(sums)

    if language_one == PYTHON and language_two == CPP or language_one == CPP and language_two == PYTHON:
        if py and cpp:
            for key_py, key_cpp in zip(py.keys(), cpp.keys()):
                python_body = py[key_py]
                cpp_body = cpp[key_cpp]
                python_body_splitted = sanitize_python_body(python_body)
                cpp_body_splitted = sanitize_java_cpp_body(cpp_body)
                for python_line, cpp_line in zip(python_body_splitted, cpp_body_splitted):
                    sums.append(compare_line(python_line, cpp_line))
                findings[key_py] = statistics.median(sums)
    if language_one == JAVA and language_two == CPP or language_one == CPP and language_two == JAVA:
        for key_java, key_cpp in zip(jv.keys(), cpp.keys()):
            java_body = jv[key_java]
            cpp_body = cpp[key_cpp]
            java_body_splitted = sanitize_java_cpp_body(java_body)
            cpp_body_splitted = sanitize_java_cpp_body(cpp_body)
            for java_line, cpp_line in zip(java_body_splitted, cpp_body_splitted):
                sums.append(compare_line(java_line, cpp_line))
            findings[key_java] = statistics.median(sums)

    return findings


def compare_line(line_one, line_two):
    """compares lines and gives an estimate on equality"""
    equality = []
    line_one_exploded = line_one.split()
    line_two_exploded = line_two.split()
    for item_one, item_two in zip(line_one_exploded, line_two_exploded):
        equality.append(fuzz.ratio(item_one, item_two))
    return statistics.median(equality)


def extract_java_functions(jv_dict):
    """sanitize java functions from class names"""
    sanitized = {}
    for value in jv_dict.values():
        sanitized.update(value)
    return sanitized


def split_strings(sample_string):
    """splits lines from input"""
    return sample_string.splitlines()


def sanitize_python_body(sample_string):
    """returns a python body without function head"""
    final_strings = []
    strings = split_strings(sample_string)
    for line in strings:
        if "def" not in line:
            final_strings.append(line)
    return final_strings

def sanitize_java_cpp_body(sample_string):
    """returns a java/cpp body without clauses"""
    final_strings = []
    matches = ["{","}"]
    strings = split_strings(sample_string)
    for line in strings:
        if not any(x in line for x in matches):
            final_strings.append(line)
    return final_strings
 
# generate language code from extracted information
if __name__ == "__main__":

    py = create_hugger(PYTHON)
    jv = create_hugger(JAVA)
    cpp = create_hugger(CPP)

    py.parse_file("self_made_dataset/python/one.py")
    jv.parse_file("self_made_dataset/java/one.java")
    cpp.parse_file("self_made_dataset/cpp/one.cpp")

    # py_function_names = py.get_all_class_method_names()
    # jv_function_names = jv.get_all_class_method_names()
    # cpp_function_names = cpp.get_all_function_names()

    # py_function_heads = py.get_all_function_names_with_params()
    # jv_function_heads = extract_java_functions(jv.get_all_method_names_with_params())
    # cpp_function_heads = cpp.get_all_function_names_with_params()

    # print(compare_function_heads(PYTHON,JAVA,py_function_heads,jv_function_heads,cpp_function_heads))

    py_function_bodies = py.get_all_function_bodies()
    jv_function_bodies = jv.get_all_method_bodies()
    cpp_function_bodies = cpp.get_all_function_bodies()

    print("------------_PYTHON_-----------------")
    print(py_function_bodies["test"])
    print("------------_JAVA_-----------------")
    print(extract_java_functions(jv_function_bodies)["test"])
    print("------------_CPP_-----------------")
    print(cpp_function_bodies["test"])

    print(compare_function_bodies(PYTHON,JAVA, py_function_bodies, extract_java_functions(jv_function_bodies)))
